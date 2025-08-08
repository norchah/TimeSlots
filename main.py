import logging

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db.db import get_db, SessionLocal, Base, engine
from models import RoleDB, UserDB, user_roles
from routers.auth import auth_router
from routers.bookings import booking_router
from routers.roles import roles_router
from routers.timeslots import time_slot_router
from routers.users import user_router

logger = logging.getLogger(__name__)

# Создаем приложение FastApi
app = FastAPI(title="TimeSlotRU MVP")

origins = [
    "http://localhost:3000",
    "http://172.18.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["set-cookie"],
)

# Подключаем роуты
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(roles_router)
app.include_router(time_slot_router)
app.include_router(booking_router)

# Автомиграция
Base.metadata.create_all(bind=engine)


# Создание ролей
def init_roles_and_admin(db: Session = Depends(get_db)):
    roles = [
        {"name": "admin", "description": "Full access to manage roles and resources"},
        {"name": "client", "description": "Can book services"}

    ]
    for role in roles:
        # Проверяем, существует ли роль
        existing_role = db.query(RoleDB).filter(RoleDB.name == role["name"]).first()
        if not existing_role:
            logger.debug(f"Role {role['name']} not found. Creating it.")
            new_role = RoleDB(name=role["name"], description=role["description"])
            db.add(new_role)
            db.commit()  # Фиксируем роль сразу после добавления
            db.refresh(new_role)
            logger.debug(f"Role {new_role.name} created with ID {new_role.id}.")

        # Создаём пользователя admin с ролью admin, если его нет
    existing_admin = db.query(UserDB).filter(UserDB.username == "admin").first()
    if not existing_admin:
        admin_role = db.query(RoleDB).filter(RoleDB.name == "admin").first()
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


# Выполняем инициализацию при старте
with SessionLocal() as db:
    init_roles_and_admin(db)

if __name__ == '__main__':
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        ssl_keyfile="certs/localhost+2-key.pem",
        ssl_certfile="certs/localhost+2.pem",
    )
