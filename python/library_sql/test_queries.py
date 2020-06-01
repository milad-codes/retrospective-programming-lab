import unittest

from library_sql.queries import NoCopyAvailable, borrow, connect, monthly_loans, overdue, top_borrowers


class LibraryTest(unittest.TestCase):
    def setUp(self):
        self.db = connect()
        self.db.executemany("INSERT INTO members (id, name, joined_on) VALUES (?, ?, ?)",
                            [(1, "Avery", "2020-01-05"), (2, "Blake", "2020-02-10"), (3, "Casey", "2020-03-15")])
        self.db.executemany("INSERT INTO books (id, title, author, copies) VALUES (?, ?, ?, ?)",
                            [(1, "Sample Algorithms", "A. Author", 1), (2, "Example Databases", "B. Writer", 2)])

    def tearDown(self):
        self.db.close()

    def test_borrow_respects_the_number_of_copies(self):
        borrow(self.db, 1, 1, "2021-01-01", "2021-01-15")
        with self.assertRaises(NoCopyAvailable):
            borrow(self.db, 1, 2, "2021-01-02", "2021-01-16")
        borrow(self.db, 2, 2, "2021-01-02", "2021-01-16")
        borrow(self.db, 2, 3, "2021-01-03", "2021-01-17")
        with self.assertRaises(LookupError):
            borrow(self.db, 99, 1, "2021-01-03", "2021-01-17")

    def test_a_failed_borrow_leaves_no_open_transaction(self):
        borrow(self.db, 1, 1, "2021-01-01", "2021-01-15")
        with self.assertRaises(NoCopyAvailable):
            borrow(self.db, 1, 2, "2021-01-01", "2021-01-15")
        self.assertFalse(self.db.in_transaction)
        self.assertEqual(self.db.execute("SELECT count(*) FROM loans").fetchone()[0], 1)

    def test_constraints_reject_impossible_dates(self):
        with self.assertRaises(Exception):
            borrow(self.db, 2, 1, "2021-01-10", "2021-01-01")

    def test_overdue_report(self):
        borrow(self.db, 1, 1, "2021-01-01", "2021-01-15")
        loan = borrow(self.db, 2, 2, "2021-01-01", "2021-01-10")
        borrow(self.db, 2, 3, "2021-01-05", "2021-02-01")
        self.db.execute("UPDATE loans SET returned_on = '2021-01-09' WHERE id = ?", (loan,))
        rows = overdue(self.db, "2021-01-20")
        self.assertEqual([(r["name"], r["days_overdue"]) for r in rows], [("Avery", 5)])

    def test_top_borrowers_shares_ranks_on_ties(self):
        for month in range(1, 4):
            borrow(self.db, 2, 1, f"2021-0{month}-01", f"2021-0{month}-10")
            self.db.execute("UPDATE loans SET returned_on = due_on")
        borrow(self.db, 2, 2, "2021-05-01", "2021-05-10")
        borrow(self.db, 1, 3, "2021-05-01", "2021-05-10")
        rows = top_borrowers(self.db)
        self.assertEqual([(r["name"], r["loans"], r["rank"]) for r in rows],
                         [("Avery", 3, 1), ("Blake", 1, 2), ("Casey", 1, 2)])

    def test_monthly_running_total(self):
        borrow(self.db, 2, 1, "2021-01-03", "2021-01-10")
        borrow(self.db, 2, 2, "2021-01-04", "2021-01-11")
        self.db.execute("UPDATE loans SET returned_on = due_on")
        borrow(self.db, 2, 3, "2021-03-01", "2021-03-10")
        self.assertEqual([tuple(r) for r in monthly_loans(self.db)], [("2021-01", 2, 2), ("2021-03", 1, 3)])


if __name__ == "__main__":
    unittest.main()
