from pydantic import BaseModel

from app.schemas.user import UserRead


class LoginRequest(BaseModel):
    is_guest: bool
    username: str | None = None
    password: str | None = None


class LoginResponse(BaseModel):
    user: UserRead
    access_token: str
    token_type: str = "bearer"

class SignUpRequest(BaseModel):
    username: str
    password: str
    current_username: str | None = None  # Optional field for the current username

class SignUpResponse(BaseModel):
    user: UserRead
    access_token: str
    token_type: str = "bearer"