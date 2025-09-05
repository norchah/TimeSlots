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


def delete_instance_from_db(db: Session, instance):
    """
    Удаляет экземпляр модели из базы данных.

    Выполняет удаление объекта из текущей сессии SQLAlchemy,
    коммитит изменения и гарантирует, что объект больше не привязан к сессии.

    Args:
        db (Session): Активная сессия SQLAlchemy.
        instance: Экземпляр модели SQLAlchemy, который необходимо удалить.

    Returns:
        None
    """
    db.delete(instance)
    db.commit()


def save_instances_to_db(db: Session, instances: list):
    """
    Сохраняет список экземпляров моделей в базу данных.

    Добавляет все экземпляры в текущую сессию SQLAlchemy,
    выполняет коммит, а затем обновляет каждый объект из базы.

    Args:
        db (Session): Активная сессия SQLAlchemy.
        instances (list): Список экземпляров моделей SQLAlchemy, которые необходимо сохранить.

    Returns:
        list: Список обновлённых экземпляров моделей с актуальными данными из БД.

    Пример использования:
        schedule_objs = [
            UserSchedule(provider_id=1, weekday=1, start_time=datetime(...), end_time=datetime(...)),
            UserSchedule(provider_id=1, weekday=2, start_time=datetime(...), end_time=datetime(...)),
        ]
        save_instances_to_db(db, schedule_objs)
    """
    if not instances:
        return []

    db.add_all(instances)
    db.commit()

    for instance in instances:
        db.refresh(instance)

    return instances
