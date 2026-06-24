import uuid
from datetime import datetime

from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.auth import LoginRequest, SignUpRequest

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def login(payload: LoginRequest, db: AsyncSession) -> User:
    if payload.is_guest:
        user = User(
            username=f"Guest_{uuid.uuid4().hex[:8]}",
            is_anonymous=True,
            personal_vector=None,
            last_active_at=datetime.now(),
        )
        db.add(user)
    else:
        result = await db.execute(select(User).where(User.username == payload.username))
        user = result.scalar_one_or_none()
        if not user or not pwd_context.verify(payload.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        user.last_active_at = datetime.now()

    await db.commit()
    await db.refresh(user)
    return user


async def sign_up(payload: SignUpRequest, db: AsyncSession) -> User:
    result = await db.execute(select(User).where(User.username == payload.username))
    if result.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail="Username already taken")

    password_hash = pwd_context.hash(payload.password)

    if payload.current_username:
        result = await db.execute(select(User).where(User.username == payload.current_username))
        user = result.scalar_one_or_none()
        if not user or not user.is_anonymous:
            raise HTTPException(status_code=404, detail="Guest user not found")
        user.username = payload.username
        user.password_hash = password_hash
        user.is_anonymous = False
    else:
        user = User(
            username=payload.username,
            password_hash=password_hash,
            is_anonymous=False,
            personal_vector=None,
        )
        db.add(user)

    user.last_active_at = datetime.now()
    await db.commit()
    await db.refresh(user)
    return user