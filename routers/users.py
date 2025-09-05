import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import models.users as models
import schemas.users as schemas
from crud.users import crud_delete_user, crud_add_role_to_user, crud_become_provider
from db.db import get_db

user_router = APIRouter(prefix="/users", tags=["Users"])

logger = logging.getLogger(__name__)


@user_router.get("/", response_model=list[schemas.UserResponse], status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.UserDB).all()


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    crud_delete_user(db, user_id)
    return {"status_code": 204, "detail": "User deleted"}


@user_router.post("/{user_id}/role/{role_id}/", response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def add_user_role(user_id: str, role_id: int,
                  db: Session = Depends(get_db)):
    # current_user: dict = Depends(get_current_user), //TODO это добавить в в аргументы ф-ции
    # Проверяем, что вызывающий пользователь — админ
    # if "admin" not in current_user["roles"]:
    #     raise HTTPException(status_code=403, detail="Not enough permissions")

    return crud_add_role_to_user(db, user_id, role_id)


@user_router.post("/become_provider/{user_id}", status_code=status.HTTP_200_OK)
def become_provider(user_id: str, db: Session = Depends(get_db)):
    return crud_become_provider(db, user_id)
