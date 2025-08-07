import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from db import get_db
from utils.auth import get_current_user

user_router = APIRouter(prefix="/users", tags=["Users"])

logger = logging.getLogger(__name__)


@user_router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Проверяем, что пользователь не существует
    db_user = db.query(models.UserDB).filter(models.UserDB.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, details="User already exist")
    # Находим роль, что б взять id
    client_role = db.query(models.RoleDB).filter(models.RoleDB.name == "client").first()
    logger.warning(f'client_role: {client_role}')
    # Создаем пользователя
    new_user = models.UserDB(**user.dict())
    db.add(new_user)
    # Получаем id пользователя
    db.flush()
    # Добавляем ему роль
    db.execute(models.user_roles.insert().values(user_id=new_user.id, role_id=client_role.id))
    db.commit()
    db.refresh(new_user)
    return new_user


@user_router.get("/", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.UserDB).all()


@user_router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.UserDB).filter(models.UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"status_code": 204, "detail": "User deleted"}


@user_router.post("/{user_id}/role/{role_id}/", response_model=schemas.UserResponse)
def add_user_role(user_id: int, role_id: int, current_user: dict = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    logger.debug(f"Checking if user {current_user['user_id']} has admin role")
    # Проверяем, что вызывающий пользователь — админ
    if "admin" not in current_user["roles"]:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    # Проверяем существование пользователя
    user = db.query(models.UserDB).filter(models.UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Проверяем существование роли
    role = db.query(models.RoleDB).filter(models.RoleDB.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
        # Добавляем роль
    logger.debug(f"Assigning role {role.name} (ID: {role_id}) to user (ID: {user_id})")
    db.execute(models.user_roles.insert().values(user_id=user_id, role_id=role_id))
    db.commit()
    db.refresh(user)
    return schemas.UserResponse(
        id=user.id,
        username=user.username,
        roles=[schemas.RoleResponse(id=r.id, name=r.name, description=r.description) for r in user.roles]
    )
