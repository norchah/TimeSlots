import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

import schemas.users as schemas
from db.instance_base import save_instance_to_db, delete_instance_from_db
from db.user_crud_base import get_user_by_username_from_db, get_role_by_name_from_db, get_user_by_id_from_db, \
    raise_if_user_exists, get_user_or_404, get_role_or_404, get_role_by_id_from_db, create_user_in_db

logger = logging.getLogger(__name__)


def crud_create_user(db: Session, user: schemas.UserCreate):
    # Проверяем, что пользователь не существует
    raise_if_user_exists(get_user_by_username_from_db(db, user.username))
    # Создаем пользователя в памяти (не добавляем в БД сразу)
    new_user = create_user_in_db(user)
    # Достаем роль "client" и проверяем, что она существует
    role_named_client = get_role_or_404(get_role_by_name_from_db(db, "client"))
    # Добавляем роль через relationship
    new_user.roles.append(role_named_client)
    # Сохраняем пользователя с ролями в БД через универсальную функцию
    new_user = save_instance_to_db(db, new_user)
    return new_user


def crud_get_user(db: Session, user_id: str | None = None, username: str | None = None):
    """Получает и возвращает пользователя по id или по username"""
    if not user_id and not username:
        raise HTTPException(status_code=400, detail="Either user_id or username must be provided")
    if user_id is not None:
        user = get_user_or_404(get_user_by_id_from_db(db, user_id))
    else:  # username is not None
        user = get_user_or_404(get_user_by_username_from_db(db, username))
    return user


def crud_delete_user(db: Session, user_id: str):
    user = get_user_or_404(get_user_by_id_from_db(db, user_id))
    delete_instance_from_db(db, user)


def crud_add_role_to_user(db: Session, user_id: str, role_id: int):
    # Получаем пользователя и роль (с авто-raise 404)
    user = get_user_or_404(get_user_by_id_from_db(db, user_id))
    role = get_role_or_404(get_role_by_id_from_db(db, role_id))
    # Добавляем роль через relationship
    if role not in user.roles:
        user.roles.append(role)
    # Сохраняем изменения через универсальную функцию
    return save_instance_to_db(db, user)


def crud_delete_role(db: Session, role_id: int):
    role = get_role_or_404(get_role_by_id_from_db(db, role_id))
    delete_instance_from_db(db, role)


def crud_become_provider(db: Session, user_id: str):
    # Получаем пользователя или кидаем 404
    user = get_user_or_404(get_user_by_id_from_db(db, user_id))
    # Проверяем, есть ли уже роль провайдера
    provider_role = get_role_or_404(get_role_by_name_from_db(db, 'provider'))
    if any(role.id == provider_role.id for role in user.roles):
        raise HTTPException(status_code=400, detail="User is already a provider")
    # Добавляем роль провайдера
    crud_add_role_to_user(db, user_id, provider_role.id)
    return user