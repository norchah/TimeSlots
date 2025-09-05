from datetime import date, timedelta

from dateutil.relativedelta import relativedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session

from db.instance_base import save_instances_to_db, save_instance_to_db
from models.schedule import ScheduleDB, ShiftDB, ShiftPatternsDB


# ---------------------------
# Инициализация пустого расписания 7 дней
# ---------------------------
def init_empty_schedule_for_provider(db: Session, provider_id: str):
    """
    Создаёт пустое расписание на 7 дней для нового провайдера.
    """
    schedules = []
    for weekday in range(1, 8):  # 1..7
        schedules.append(ScheduleDB(
            provider_id=provider_id,
            weekday=weekday,
            is_available=False,
            schedule_start_time=None,
            schedule_end_time=None,
        ))
    schedules_db = save_instances_to_db(db, schedules)
    return schedules_db


# ---------------------------
# Инициализация пустого расписания 2/2 и т.п. дней
# ---------------------------
def init_shift_schedule_for_provider(
        db: Session,
        provider_id: str,
        pattern: str,
        months_ahead: int = 1,
):
    """
    Создаёт сменное расписание для провайдера по указанному паттерну.

    Args:
        db (Session): SQLAlchemy сессия.
        provider_id (str): ID провайдера.
        pattern (str): строка в формате "2/2", "3/1" и т.п. (рабочие/выходные).
        months_ahead (int): На сколько месяцев вперёд сгенерировать расписание.

    Returns:
        list[UserShift]: Список созданных смен.
    """
    # парсим паттерн
    try:
        work_days, off_days = map(int, pattern.split("/"))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid shift pattern format. Use 'X/Y'.")

    # дата начала с сегодняшнего дня
    today = date.today()
    end_date = today + relativedelta(months=months_ahead)

    shifts: list[ShiftDB] = []
    current_start = today
    is_working = True

    while current_start < end_date:
        duration = work_days if is_working else off_days
        current_end = current_start + timedelta(days=duration - 1)

        if is_working:
            shift = ShiftDB(
                provider_id=provider_id,
                start_time=current_start,
                end_time=current_end,
            )
            shifts.append(shift)

        # следующая смена
        current_start = current_end + timedelta(days=1)
        is_working = not is_working

    # сохраняем
    save_instances_to_db(db, shifts)
    # также фиксируем сам паттерн (в отдельной таблице)
    pattern_entry = ShiftPatternsDB(provider_id=provider_id, pattern=pattern)
    save_instance_to_db(db, pattern_entry)

    return shifts
