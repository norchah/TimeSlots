from pydantic import BaseModel, Field


class RoleCreate(BaseModel):
    name: str = Field(..., min_length=3)
    description: str | None = None


class RoleResponse(BaseModel):
    id: int
    name: str
    description: str | None = None


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    first_name: str | None = Field(default=None, min_length=3)
    last_name: str | None = Field(default=None, min_length=3)


class UserResponse(BaseModel):
    id: str
    username: str
    first_name: str | None
    last_name: str | None
    roles: list[RoleResponse]
