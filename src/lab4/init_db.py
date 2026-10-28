from pathlib import Path

import psycopg

DSN = "postgresql://postgres:postgres@localhost:5432/lab4"

SCHEMA_FILE = Path(__file__).resolve().parents[2] / "sql" / "schema.sql"

ROLES = [
    ("admin", "Повний доступ до системи"),
    ("editor", "Може редагувати контент"),
    ("moderator", "Модерує користувачів і контент"),
    ("viewer", "Лише перегляд"),
    ("guest", "Обмежений гостьовий доступ"),
]

GROUPS = [
    ("Developers", "Розробники"),
    ("Designers", "Дизайнери"),
    ("Testers", "Тестувальники"),
    ("Managers", "Менеджери"),
    ("Support", "Служба підтримки"),
    ("Security", "Команда безпеки"),
    ("Analytics", "Аналітики"),
    ("Students", "Студенти"),
]

FIRST_NAMES = [
    "Іван",
    "Олена",
    "Андрій",
    "Марія",
    "Петро",
    "Наталія",
    "Олег",
    "Софія",
    "Тарас",
    "Ірина",
]
LAST_NAMES = ["Коваленко", "Шевченко", "Бондаренко", "Ткачук"]

USERS_COUNT = 40


def build_users() -> list[tuple[str, str, str, int]]:
    """Генерує 40 користувачів: (ім'я, email, телефон, id ролі)."""
    users = []
    for i in range(USERS_COUNT):
        full_name = f"{FIRST_NAMES[i % 10]} {LAST_NAMES[i // 10]}"
        email = f"user{i + 1}@example.com"
        phone = f"+38050{1000000 + i}"
        role_id = i % len(ROLES) + 1
        users.append((full_name, email, phone, role_id))
    return users


def build_user_groups() -> list[tuple[int, int]]:
    """Кожен користувач потрапляє у 2 групи: пари (id користувача, id групи)."""
    pairs = []
    for user_id in range(1, USERS_COUNT + 1):
        first = user_id % len(GROUPS) + 1
        second = (user_id + 3) % len(GROUPS) + 1
        pairs.append((user_id, first))
        pairs.append((user_id, second))
    return pairs


def init_db() -> None:
    schema_sql = SCHEMA_FILE.read_text(encoding="utf-8")
    with psycopg.connect(DSN) as conn:
        conn.execute(schema_sql)
        conn.execute(
            "TRUNCATE user_groups, users, groups, roles RESTART IDENTITY CASCADE"
        )
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO roles (name, description) VALUES (%s, %s)", ROLES
            )
            cur.executemany(
                "INSERT INTO groups (name, description) VALUES (%s, %s)", GROUPS
            )
            cur.executemany(
                "INSERT INTO users (full_name, email, phone, role_id) "
                "VALUES (%s, %s, %s, %s)",
                build_users(),
            )
            cur.executemany(
                "INSERT INTO user_groups (user_id, group_id) VALUES (%s, %s)",
                build_user_groups(),
            )
    print("База даних ініціалізована.")


if __name__ == "__main__":
    init_db()
