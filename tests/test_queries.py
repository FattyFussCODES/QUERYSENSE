from __future__ import annotations

import os
import tempfile
import unittest


from config.db_config import get_db_config
from database.init_db import init_db
from engine.query_service import run_nl_query
from executor.db_connection import create_connection


class TestEndToEndSQLite(unittest.TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory()
        self._db_path = os.path.join(self._tmpdir.name, "test_querysense.db")

        os.environ["DB_DIALECT"] = "sqlite"
        os.environ["DB_PATH"] = self._db_path

        init_db()

    def tearDown(self) -> None:
        self._tmpdir.cleanup()

    def test_count_students(self) -> None:
        config = get_db_config()
        conn = create_connection(config)
        try:
            result = run_nl_query(conn, "count students")
            self.assertEqual(result["columns"], ["count"])
            self.assertGreater(result["rows"][0][0], 8) # Accommodating new larger schema
        finally:
            conn.close()

    def test_marks_filter(self) -> None:
        config = get_db_config()
        conn = create_connection(config)
        try:
            result = run_nl_query(conn, "show students with marks above 2000")
            marks_idx = result["columns"].index("marks")
            self.assertTrue(all(r[marks_idx] > 2000 for r in result["rows"]))
        finally:
            conn.close()

    def test_gpa_filter(self) -> None:
        config = get_db_config()
        conn = create_connection(config)
        try:
            result = run_nl_query(conn, "students with gpa above 9.0")
            gpa_idx = result["columns"].index("gpa")
            self.assertTrue(all(r[gpa_idx] > 9.0 for r in result["rows"]))
        finally:
            conn.close()

    def test_top_n(self) -> None:
        config = get_db_config()
        conn = create_connection(config)
        try:
            result = run_nl_query(conn, "top 2 students")
            self.assertEqual(len(result["rows"]), 2)
            gpa_idx = result["columns"].index("gpa")
            self.assertGreaterEqual(result["rows"][0][gpa_idx], result["rows"][1][gpa_idx])
        finally:
            conn.close()


if __name__ == "__main__":
    unittest.main()
