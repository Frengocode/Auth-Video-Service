from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from .token import SECRET_KEY, ALGORITHM
from src.services.user_service import models
from src.core.databse import get_user_service_session
from sqlalchemy.orm import Session
from .scheme import TokenData
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

async def get_current_user(token: str = Depends(oauth2_schema), session: AsyncSession = Depends(get_user_service_session)) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    result = await session.execute(
        select(models.User).where(models.User.username == token_data.username)
    )
    
    user = result.scalars().first()

    if user is None:
        raise credentials_exception

    return user