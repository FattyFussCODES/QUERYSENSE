-- QuerySense Leaderboard Schema
-- Compatible with database/init_db.py

DROP TABLE IF EXISTS students;

CREATE TABLE IF NOT EXISTS students (
	enroll_no TEXT PRIMARY KEY,
	name TEXT NOT NULL,
	marks INTEGER NOT NULL,
	gpa REAL NOT NULL,
	rank INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_students_marks ON students(marks);
CREATE INDEX IF NOT EXISTS ix_students_gpa ON students(gpa);
CREATE INDEX IF NOT EXISTS ix_students_rank ON students(rank);
