from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str | None = None
    is_anonymous: bool = False
    personal_vector: list[float] | None = None


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_anonymous: bool
    personal_vector: list[float] | None = None
    created_at: datetime
    last_active_at: datetime | None = None
