from fastapi import HTTPException

from models.users import UserDB, RoleDB


def create_user_in_db(user):
    return UserDB(**user.dict())


def get_user_by_id_from_db(db, user_id):
    """Извлекает и возвращает пользователя из БД по id"""
    return db.query(UserDB).filter(UserDB.id == user_id).first()


def get_user_by_username_from_db(db, username):
    """Извлекает и возвращает пользователя из БД по username"""
    return db.query(UserDB).filter(UserDB.username == username).first()


def get_role_by_name_from_db(db, name):
    """Извлекает и возвращает роль из БД по имени"""
    return db.query(RoleDB).filter(RoleDB.name == name).first()


def get_role_by_id_from_db(db, role_id):
    """Извлекает и возвращает роль из БД по id"""
    return db.query(RoleDB).filter(RoleDB.id == role_id).first()


def get_user_or_404(user):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def raise_if_user_exists(user):
    if user:
        raise HTTPException(status_code=400, detail="User already exist")
    return user


def get_role_or_404(role):
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


def raise_if_role_exists(role):
    if role:
        raise HTTPException(status_code=400, detail="User already exist")
    return role
