from abc import ABC, abstractmethod
from typing import Any

import psycopg
from psycopg.rows import dict_row

DSN = "postgresql://postgres:postgres@localhost:5432/lab4"

COLUMNS = "id, full_name, email, phone, role_id, created_at"


class UserRepository(ABC):
    """Абстракція сховища користувачів. API залежить лише від неї."""

    @abstractmethod
    def list_users(self) -> list[dict[str, Any]]: ...

    @abstractmethod
    def get_user(self, user_id: int) -> dict[str, Any] | None: ...

    @abstractmethod
    def create_user(
        self, full_name: str, email: str, phone: str, role_id: int
    ) -> dict[str, Any]: ...

    @abstractmethod
    def update_user(
        self, user_id: int, full_name: str, email: str, phone: str, role_id: int
    ) -> dict[str, Any] | None: ...

    @abstractmethod
    def delete_user(self, user_id: int) -> bool: ...


class PostgresUserRepository(UserRepository):
    """Реалізація сховища на PostgreSQL."""

    def __init__(self, dsn: str = DSN) -> None:
        self._dsn = dsn

    def list_users(self) -> list[dict[str, Any]]:
        with psycopg.connect(self._dsn, row_factory=dict_row) as conn:
            return conn.execute(f"SELECT {COLUMNS} FROM users ORDER BY id").fetchall()

    def get_user(self, user_id: int) -> dict[str, Any] | None:
        with psycopg.connect(self._dsn, row_factory=dict_row) as conn:
            return conn.execute(
                f"SELECT {COLUMNS} FROM users WHERE id = %s",
                (user_id,),
            ).fetchone()

    def create_user(
        self, full_name: str, email: str, phone: str, role_id: int
    ) -> dict[str, Any]:
        with psycopg.connect(self._dsn, row_factory=dict_row) as conn:
            row = conn.execute(
                "INSERT INTO users (full_name, email, phone, role_id) "
                f"VALUES (%s, %s, %s, %s) RETURNING {COLUMNS}",
                (full_name, email, phone, role_id),
            ).fetchone()
        assert row is not None
        return row

    def update_user(
        self, user_id: int, full_name: str, email: str, phone: str, role_id: int
    ) -> dict[str, Any] | None:
        with psycopg.connect(self._dsn, row_factory=dict_row) as conn:
            return conn.execute(
                "UPDATE users SET full_name = %s, email = %s, phone = %s, "
                f"role_id = %s WHERE id = %s RETURNING {COLUMNS}",
                (full_name, email, phone, role_id, user_id),
            ).fetchone()

    def delete_user(self, user_id: int) -> bool:
        with psycopg.connect(self._dsn) as conn:
            cur = conn.execute("DELETE FROM users WHERE id = %s", (user_id,))
            return cur.rowcount > 0
