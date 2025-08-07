from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from db import get_db
from models import UserDB
from schemas import LoginRequest, TokenResponse
from utils.auth import create_access_token

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

    return TokenResponse(token_type="bearer", roles=roles)

@auth_router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"status": "logged out"}
