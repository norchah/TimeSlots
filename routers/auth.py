import logging

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from crud.users import crud_get_user, crud_create_user
from db.db import get_db
from db.user_crud_base import get_user_or_404
from schemas.times import LoginRequest
from schemas.users import UserResponse, UserCreate
from utils.auth import create_access_token, get_current_user, set_jwt_cookie, del_jwt_cookie

logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(request: UserCreate, response: Response, db: Session = Depends(get_db)):
    new_user = crud_create_user(db, request)
    roles = [role.name for role in new_user.roles]
    access_token = create_access_token(data={"user_id": new_user.id, "roles": roles})
    # Устанавливаем HTTP-only cookie
    set_jwt_cookie(response, access_token)
    logger.debug(f"Set cookie with token for user {request.username}: {access_token}")
    return new_user


@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = crud_get_user(db, username=request.username)
    # Получаем роли пользователя
    roles = [role.name for role in user.roles]
    # Создаём JWT с user_id и ролями
    access_token = create_access_token(data={"user_id": user.id, "roles": roles})
    # Устанавливаем HTTP-only cookie
    set_jwt_cookie(response, access_token)
    logger.debug(f"Set cookie with token for user {request.username}: {access_token}")
    return user


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
def logout(response: Response):
    del_jwt_cookie(response)
    return {"detail": "logged out"}


@auth_router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user["user_id"]
    user = get_user_or_404(crud_get_user(db, user_id=user_id))
    return user
