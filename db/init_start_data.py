import logging

from fastapi import Depends
from sqlalchemy.orm import Session

from db.db import get_db
from db.user_crud_base import get_role_by_name_from_db, get_user_by_username_from_db
from models.users import RoleDB, UserDB, user_roles

logger = logging.getLogger(__name__)


def init_roles_and_admin(db: Session = Depends(get_db)):
    roles = [
        {"name": "admin", "description": "Full access to manage roles and resources"},
        {"name": "client", "description": "Can book services"},
        {"name": "provider", "description": "Can create schedule"}
    ]
    for role in roles:
        # Проверяем, существует ли роль
        existing_role = get_role_by_name_from_db(db, role["name"])
        if not existing_role:
            logger.debug(f"Role {role['name']} not found. Creating it.")
            new_role = RoleDB(name=role["name"], description=role["description"])
            db.add(new_role)
            db.commit()  # Фиксируем роль сразу после добавления
            db.refresh(new_role)
            logger.debug(f"Role {new_role.name} created with ID {new_role.id}.")

        # Создаём пользователя admin с ролью admin, если его нет
    existing_admin = get_user_by_username_from_db(db, 'admin')
    if not existing_admin:
        admin_role = get_role_by_name_from_db(db, "admin")
        if not admin_role:
            raise RuntimeError("Admin role not initialized")
        admin_user = UserDB(username="admin")
        db.add(admin_user)
        db.flush()  # Получаем ID пользователя
        db.execute(user_roles.insert().values(user_id=admin_user.id, role_id=admin_role.id))
        db.commit()
        logger.debug("Admin user created with admin role.")
    else:
        logger.debug("Admin user already exists.")
