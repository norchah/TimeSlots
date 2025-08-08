import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from db.instance_base import save_instance_to_db
from db.user_crud_base import get_user_by_username_from_db, get_role_by_name_from_db, get_user_by_id_from_db

logger = logging.getLogger(__name__)


def create_user(db: Session, user: schemas.UserCreate):
    # Проверяем, что пользователь не существует
    if get_user_by_username_from_db(db, user.username):
        raise HTTPException(status_code=400, detail="User already exist")
    # Создаем пользователя
    new_user = models.UserDB(**user.dict())
    # Достаем роль
    role_named_client = get_role_by_name_from_db(db, "client")
    # Сохраняем в БД
    new_user = save_instance_to_db(db, new_user)
    # Добавляем роль
    db.execute(models.user_roles.insert().values(
        user_id=new_user.id,
        role_id=role_named_client.id,
    ))
    # Еще раз комитим
    db.commit()
    return new_user


def get_user(db: Session, user_id: int | None = None, username: str | None = None):
    """Получает и возвращает пользователя по id или по username"""
    if not user_id and not username:
        raise HTTPException(status_code=400, detail="Either user_id or username must be provided")
    user = None
    if user_id is not None:
        user = get_user_by_id_from_db(db, user_id)
    elif username is not None:
        user = get_user_by_username_from_db(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
