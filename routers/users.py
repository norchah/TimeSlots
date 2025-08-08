import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from db.db import get_db
from db.user_crud_base import get_user_by_id_from_db, get_role_by_id_from_db
from utils.auth import get_current_user

user_router = APIRouter(prefix="/users", tags=["Users"])

logger = logging.getLogger(__name__)


@user_router.get("/", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.UserDB).all()


@user_router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id_from_db(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"status_code": 204, "detail": "User deleted"}


@user_router.post("/{user_id}/role/{role_id}/", response_model=schemas.UserResponse)
def add_user_role(user_id: int, role_id: int, current_user: dict = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    # Проверяем, что вызывающий пользователь — админ
    if "admin" not in current_user["roles"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    # Проверяем существование пользователя
    user = get_user_by_id_from_db(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Проверяем существование роли
    role = get_role_by_id_from_db(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
        # Добавляем роль
    db.execute(models.user_roles.insert().values(user_id=user_id, role_id=role_id))
    db.commit()
    db.refresh(user)
    return user
