from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas
from db.db import get_db

roles_router = APIRouter(tags=["Roles"])


@roles_router.post("/roles/", response_model=schemas.RoleResponse)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    db_role = db.query(models.RoleDB).filter(models.RoleDB.name == role.name).first()
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    new_role = models.RoleDB(
        name=role.name,
        description=role.description,
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role


@roles_router.get("/roles/", response_model=list[schemas.RoleResponse])
def get_all_roles(db: Session = Depends(get_db)):
    return db.query(models.RoleDB).all()


@roles_router.delete("/roles/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(models.RoleDB).filter(models.RoleDB.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(role)
    db.commit()
    return {"status_code": 204, "detail": "Role deleted"}
