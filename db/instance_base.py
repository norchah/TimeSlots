from sqlalchemy.orm import Session


def save_instance_to_db(db: Session, instance):
    """
    Сохраняет экземпляр модели в базу данных.

    Добавляет экземпляр в текущую сессию SQLAlchemy,
    выполняет промежуточный flush для получения значений,
    коммитит изменения и обновляет объект из базы.

    Args:
        db (Session): Активная сессия SQLAlchemy.
        instance: Экземпляр модели SQLAlchemy, который необходимо сохранить.

    Returns:
        instance: Обновлённый экземпляр модели с актуальными данными из БД.
    """
    db.add(instance)
    db.flush()
    db.commit()
    db.refresh(instance)
    return instance
