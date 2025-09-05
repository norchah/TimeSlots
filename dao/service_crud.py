from sqlalchemy.orm import Session

from models.services import ProviderServiceDB


def dao_get_provider_services(db: Session, provider_id: str):
    """Извлекает все сервисы провайдера"""
    return db.query(ProviderServiceDB).filter(ProviderServiceDB.provider_id == provider_id).all()
