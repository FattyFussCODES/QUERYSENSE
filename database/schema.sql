-- QuerySense demo schema (SQLite)
-- Compatible with database/init_db.py which executes SQL files

CREATE TABLE IF NOT EXISTS students (
	student_id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	course TEXT NOT NULL,
	marks INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_students_course ON students(course);
CREATE INDEX IF NOT EXISTS ix_students_marks ON students(marks);
