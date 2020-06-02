# Library in SQL

A lending library in SQLite (bundled with Python, so nothing to install), focused on the database rather than the
Python code:

- **constraints** in `schema.sql`: foreign keys, `CHECK` rules for copies and dates, and a partial index over open loans;
- **a race-free borrow** in `queries.py`: `BEGIN IMMEDIATE` takes the write lock before the availability check, so two
  members can't both get the last copy;
- **reports** with joins, date arithmetic and window functions: overdue loans, top borrowers with `RANK()`, monthly
  loans with a running `SUM() OVER`.

All names in the tests are invented.

```bash
python3 -m unittest discover -s library_sql -t .
```
