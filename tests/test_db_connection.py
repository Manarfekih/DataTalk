from __future__ import annotations

from datatalk.database.connection import db_manager


def test_database_connection() -> None:
   

    assert db_manager.is_connected()
