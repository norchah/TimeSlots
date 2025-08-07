from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from db import get_db
from models import UserDB
from schemas import LoginRequest, UserResponse, RoleResponse
from utils.auth import create_access_token, get_current_user

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login")
def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    # Находим пользователя по username
    user = db.query(UserDB).filter(UserDB.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Получаем роли пользователя
    roles = [role.name for role in user.roles]

    # Создаём JWT с user_id и ролями
    access_token = create_access_token(data={"user_id": user.id, "roles": roles})

    # Устанавливаем HTTP-only cookie
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # Защита от XSS
        secure=False,  # Для localhost, в проде True
        samesite="lax",  # Защита от CSRF
        max_age=30 * 60  # 30 минут
    )
    return {"user": user.id}


@auth_router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"status": "logged out"}


@auth_router.get("/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user["user_id"]
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse(
        id=user.id,
        username=user.username,
        roles=[RoleResponse(id=r.id, name=r.name, description=r.description) for r in user.roles]
    )
