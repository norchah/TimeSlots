import logging

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from crud.services import crud_create_service
from dao.service_crud import dao_get_provider_services
from db.db import get_db
from schemas.services import ServiceResponse, ServiceCreate

service_router = APIRouter(prefix="/service", tags=["Услуги"])

logger = logging.getLogger(__name__)


@service_router.post('/create', response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    return crud_create_service(db, service)


@service_router.get("/all/{provider_id}", status_code=status.HTTP_200_OK)
def get_provider_services(provider_id: str, db: Session = Depends(get_db)):
    """
    Возвращает все расписания провайдера
    """
    return dao_get_provider_services(db, provider_id)
