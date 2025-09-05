from sqlalchemy.orm import Session

from dao.service_crud import dao_get_provider_services
from db.instance_base import save_instance_to_db
from models.services import ProviderServiceDB
from schemas.services import ServiceCreate


def crud_create_service(db: Session, service_data: ServiceCreate):
    """
    Создает новый сервис провайдера
    """
    new_service = ProviderServiceDB(**service_data.dict())
    return save_instance_to_db(db, new_service)


def crud_get_provider_services(db: Session, provider_id: str):
    return dao_get_provider_services(db, provider_id)
