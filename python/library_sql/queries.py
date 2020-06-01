"""Reporting queries for the lending library. Every function takes an open sqlite3 connection."""

import sqlite3
from pathlib import Path

SCHEMA = (Path(__file__).parent / "schema.sql").read_text(encoding="utf-8")


def connect(path: str = ":memory:") -> sqlite3.Connection:
    # autocommit mode: statements commit on their own and transactions are opened explicitly where they matter
    connection = sqlite3.connect(path, isolation_level=None)
    connection.row_factory = sqlite3.Row
    connection.executescript(SCHEMA)
    return connection


class NoCopyAvailable(Exception):
    pass


def borrow(db: sqlite3.Connection, book_id: int, member_id: int, on: str, due: str) -> int:
    """Records a loan only if a copy is free. The check and the insert run in one write transaction."""
    # take the write lock before reading, so two borrowers can't both see the last free copy
    db.execute("BEGIN IMMEDIATE")
    try:
        free = db.execute(
            """SELECT b.copies - (SELECT count(*) FROM loans l WHERE l.book_id = b.id AND l.returned_on IS NULL)
                 FROM books b WHERE b.id = ?""",
            (book_id,),
        ).fetchone()
        if free is None:
            raise LookupError(f"no book with id {book_id}")
        if free[0] <= 0:
            raise NoCopyAvailable(f"all copies of book {book_id} are on loan")
        loan_id = db.execute(
            "INSERT INTO loans (book_id, member_id, borrowed_on, due_on) VALUES (?, ?, ?, ?)",
            (book_id, member_id, on, due),
        ).lastrowid
        db.execute("COMMIT")
        return loan_id
    except BaseException:
        db.execute("ROLLBACK")
        raise


def overdue(db: sqlite3.Connection, today: str) -> list[sqlite3.Row]:
    """Open loans past their due date, most overdue first, with the number of days."""
    return db.execute(
        """SELECT m.name, b.title, l.due_on,
                  CAST(julianday(?) - julianday(l.due_on) AS INTEGER) AS days_overdue
             FROM loans l JOIN members m ON m.id = l.member_id JOIN books b ON b.id = l.book_id
            WHERE l.returned_on IS NULL AND l.due_on < ?
            ORDER BY days_overdue DESC, m.name""",
        (today, today),
    ).fetchall()


def top_borrowers(db: sqlite3.Connection, limit: int = 3) -> list[sqlite3.Row]:
    """Members by number of loans, ranked with a window function (ties share a rank)."""
    return db.execute(
        """SELECT name, loans, RANK() OVER (ORDER BY loans DESC) AS rank
             FROM (SELECT m.name, count(l.id) AS loans
                     FROM members m LEFT JOIN loans l ON l.member_id = m.id
                    GROUP BY m.id)
            ORDER BY rank, name
            LIMIT ?""",
        (limit,),
    ).fetchall()


def monthly_loans(db: sqlite3.Connection) -> list[sqlite3.Row]:
    """Loans per month with a running total."""
    return db.execute(
        """SELECT month, loans, SUM(loans) OVER (ORDER BY month) AS running_total
             FROM (SELECT substr(borrowed_on, 1, 7) AS month, count(*) AS loans FROM loans GROUP BY month)
            ORDER BY month"""
    ).fetchall()
