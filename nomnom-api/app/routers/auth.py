from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, LoginResponse, SignUpRequest, SignUpResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await auth_service.login(payload, db)
    return LoginResponse(user=user, access_token=create_access_token(user.id))

@router.post("/sign-up", response_model=SignUpResponse)
async def signup(payload: SignUpRequest, db: AsyncSession = Depends(get_db)):
    user = await auth_service.sign_up(payload, db)
    return SignUpResponse(user=user, access_token=create_access_token(user.id))