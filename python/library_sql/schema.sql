-- Lending library. Dates are ISO-8601 text, which SQLite compares correctly as strings.
PRAGMA foreign_keys = ON;

CREATE TABLE members (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  joined_on TEXT NOT NULL
);

CREATE TABLE books (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  copies INTEGER NOT NULL CHECK (copies >= 0)
);

CREATE TABLE loans (
  id INTEGER PRIMARY KEY,
  book_id INTEGER NOT NULL REFERENCES books (id),
  member_id INTEGER NOT NULL REFERENCES members (id),
  borrowed_on TEXT NOT NULL,
  due_on TEXT NOT NULL,
  returned_on TEXT,
  CHECK (due_on > borrowed_on),
  CHECK (returned_on IS NULL OR returned_on >= borrowed_on)
);

CREATE INDEX loans_open_by_book ON loans (book_id) WHERE returned_on IS NULL;
