import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.db import SessionLocal, Base, engine
from db.init_start_data import init_roles_and_admin
from routers.auth import auth_router
from routers.bookings import booking_router
from routers.roles import roles_router
from routers.schedule import schedule_router
from routers.services import service_router
from routers.users import user_router

logger = logging.getLogger(__name__)

# Создаем приложение FastApi
app = FastAPI(title="TimeSlotRU MVP")

origins = [
    "http://localhost:3000",
    "https://localhost:3000",
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
app.include_router(service_router)
app.include_router(schedule_router)
app.include_router(booking_router)


# Автомиграция
Base.metadata.create_all(bind=engine)

# Создание ролей


# Выполняем инициализацию при старте
with SessionLocal() as db:
    init_roles_and_admin(db)

if __name__ == '__main__':
    uvicorn.run(
        app,
        host="localhost",
        port=8000,
        ssl_keyfile="certs/localhost+2-key.pem",
        ssl_certfile="certs/localhost+2.pem",
    )
