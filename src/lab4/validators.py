import re

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_RE = re.compile(r"^\+380\d{9}$")
NAME_RE = re.compile(r"^[A-Za-zА-Яа-яІіЇїЄєҐґ' -]{2,100}$")


def is_valid_email(value: str) -> bool:
    return EMAIL_RE.fullmatch(value) is not None


def is_valid_phone(value: str) -> bool:
    return PHONE_RE.fullmatch(value) is not None


def is_valid_name(value: str) -> bool:
    return NAME_RE.fullmatch(value) is not None
