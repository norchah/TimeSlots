from models import UserDB, RoleDB


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
