from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

import models.users as models
import schemas.users as schemas
from crud.users import crud_delete_role
from db.db import get_db
from db.instance_base import save_instance_to_db
from db.user_crud_base import get_role_by_name_from_db, get_role_or_404

roles_router = APIRouter(tags=["Roles"])


@roles_router.post("/roles/", response_model=schemas.RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    role = get_role_or_404(get_role_by_name_from_db(db, name=role.name))
    new_role = models.RoleDB(
        name=role.name,
        description=role.description,
    )
    save_instance_to_db(db, new_role)
    return new_role


@roles_router.get("/roles/", response_model=list[schemas.RoleResponse], status_code=status.HTTP_200_OK)
def get_all_roles(db: Session = Depends(get_db)):
    return db.query(models.RoleDB).all()


@roles_router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    crud_delete_role(db, role_id)
    return {"status_code": 204, "detail": "Role deleted"}
