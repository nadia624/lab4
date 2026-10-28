from dataclasses import dataclass
from datetime import datetime


@dataclass
class Role:
    """Роль користувача (наприклад, admin, editor, viewer)."""

    name: str
    description: str = ""
    id: int | None = None


@dataclass
class User:
    """Користувач системи. Кожен користувач має рівно одну роль."""

    full_name: str
    email: str
    phone: str
    role_id: int
    id: int | None = None
    created_at: datetime | None = None


@dataclass
class Group:
    """Група, до якої може належати багато користувачів."""

    name: str
    description: str = ""
    id: int | None = None


@dataclass
class UserGroup:
    """Зв'язок «користувач ↔ група» (N:M)."""

    user_id: int
    group_id: int
