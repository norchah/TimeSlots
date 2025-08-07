from sqlalchemy.orm import Session

from models import user_roles, RoleDB


def has_role(db: Session, user_id: int, required_role: str) -> bool:
    """
    Проверяет, есть ли у пользователя указанная роль.

    Args:
        db: Сессия SQLAlchemy.
        user_id: ID пользователя.
        required_role: Имя роли (например, 'client', 'provider').

    Returns:
        bool: True, если роль есть, False иначе.
    """
    return db.query(user_roles).join(RoleDB).filter(
        user_roles.c.user_id == user_id,
        RoleDB.name == required_role
    ).first() is not None
