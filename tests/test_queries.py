from __future__ import annotations

import unittest


class TestImports(unittest.TestCase):
    def test_imports(self) -> None:
        import config.db_config  # noqa: F401
        import database.init_db  # noqa: F401
        import executor.db_connection  # noqa: F401
        import engine.sql_generator  # noqa: F401


if __name__ == "__main__":
    unittest.main()
