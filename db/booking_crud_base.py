from models.bookings import BookingDB


def get_bookings_for_provider_from_db(db, provider_id):
    """
    Извлекаем все бронирования одного провайдера
    """
    return db.query(BookingDB).filter(BookingDB.provider_id == provider_id).all()


def get_bookings_for_provider_on_date_from_db(db, provider_id, target_date):
    """
    Извлекает все бронирования одного провайдера на дату
    """
    return db.query(BookingDB).filter(BookingDB.provider_id == provider_id, BookingDB.booking_date == target_date).all()


def get_bookings_for_client_on_date_from_db(db, client_id, target_date):
    """
    Извлекает все бронирования клиента на дату
    """

    return db.query(BookingDB).filter(BookingDB.client_id == client_id, BookingDB.booking_date == target_date).all()


def get_bookings_for_client_from_db(db, client_id):
    """
    Извлекает все бронирования клиента
    """
    return db.query(BookingDB).filter(BookingDB.client_id == client_id).all()


def get_bookings_for_client_provider_from_db(db, client_id, provider_id):
    """
    Извлекает все бронирования клиента у провайдера
    """
    return db.query(BookingDB).filter(BookingDB.client_id == client_id, BookingDB.provider_id == provider_id).all()


def get_bookings_for_client_provider_on_date_from_db(db, client_id, provider_id, target_date):
    """
    Извлекает все бронирования клиента у провайдера на дату
    """
    return db.query(BookingDB).filter(
        BookingDB.client_id == client_id,
        BookingDB.provider_id == provider_id,
        BookingDB.booking_date == target_date
    ).all()


def get_bookings_for_client_provider_on_date_on_time_from_db(
        db,
        client_id,
        provider_id,
        booking_date,
        start_time
):
    """
    Извлекает бронирование клиента у провайдера на дату и время
    """
    return db.query(BookingDB).filter(
        BookingDB.client_id == client_id,
        BookingDB.provider_id == provider_id,
        BookingDB.booking_date == booking_date,
        BookingDB.start_time == start_time
    ).first()
