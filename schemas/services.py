from pydantic import BaseModel


class ServiceCreate(BaseModel):
    provider_id: str
    name: str
    description: str
    duration_minutes: int
    is_group: bool
    capacity: int
    price: float


class ServiceUpdate(ServiceCreate):
    id: int


class ServiceResponse(ServiceUpdate):
    pass
