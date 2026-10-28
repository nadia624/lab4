from typing import Any

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

from lab4.repository import PostgresUserRepository, UserRepository
from lab4.validators import is_valid_email, is_valid_name, is_valid_phone

app = FastAPI(title="Lab 4: Users API")

repo: UserRepository = PostgresUserRepository()


class UserIn(BaseModel):
    full_name: str
    email: str
    phone: str
    role_id: int


def validate_user(data: UserIn) -> None:
    if not is_valid_name(data.full_name):
        raise HTTPException(status_code=422, detail="Invalid full_name")
    if not is_valid_email(data.email):
        raise HTTPException(status_code=422, detail="Invalid email")
    if not is_valid_phone(data.phone):
        raise HTTPException(
            status_code=422, detail="Invalid phone, expected +380XXXXXXXXX"
        )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/users")
def list_users() -> list[dict[str, Any]]:
    return repo.list_users()


@app.get("/users/{user_id}")
def get_user(user_id: int) -> dict[str, Any]:
    user = repo.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users", status_code=201)
def create_user(data: UserIn) -> dict[str, Any]:
    validate_user(data)
    return repo.create_user(data.full_name, data.email, data.phone, data.role_id)


@app.put("/users/{user_id}")
def update_user(user_id: int, data: UserIn) -> dict[str, Any]:
    validate_user(data)
    user = repo.update_user(
        user_id, data.full_name, data.email, data.phone, data.role_id
    )
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int) -> Response:
    if not repo.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)
