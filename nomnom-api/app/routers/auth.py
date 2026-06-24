from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import LoginRequest, LoginResponse, SignUpRequest, SignUpResponse
from app.services.auth_service import login, signUp

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
        user = await login(payload, db)
        return LoginResponse(user=user)

@router.post("/sign-up", response_model=SignUpRequest)
async def signup(payload: SignUpRequest, db: AsyncSession = Depends(get_db)):
        user = await signUp(payload, db)
        return SignUpResponse(user=user)