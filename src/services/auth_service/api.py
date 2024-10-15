from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, APIRouter, Depends
from src.services.user_service.hash import Hash
from src.services.user_service import models
from sqlalchemy import select
from .token import create_access_token
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.databse import get_user_service_session
from .scheme import SUserResponse
from src.services.user_service.models import User

auth_service = APIRouter(tags=['Auth Service'])


@auth_service.post('/auth/login/')
async def login(session: AsyncSession = Depends(get_user_service_session),  request: OAuth2PasswordRequestForm = Depends()):
    user_result = await session.execute(
        select(models.User).filter(models.User.username == request.username)
    )

    user = user_result.scalars().first()

    if not user:
        raise HTTPException(detail={"error": "Invalid Creadion"}, status_code=402)

    if not Hash.verify(request.password, user.password):
        raise HTTPException(detail=f"In Correct", status_code=402)

    access_token = create_access_token(data={"sub": user.username})
    print(access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@auth_service.get('/auth/get-user/{user_id}', response_model=SUserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_user_service_session)):

    user_query = await session.execute(

        select(User)
        .filter(User.id == user_id)
    )

    user = user_query.scalars().first()
    if not user:
        raise HTTPException(
            detail='Not Found',
            status_code=404
        )
    
    repsonse = SUserResponse(
        id = user.id,
        username = user.username
    )

    return repsonse



@auth_service.get('/auth/get-current-user/{username}', response_model=SUserResponse)
async def get_user(username: str, session: AsyncSession = Depends(get_user_service_session)):

    user_query = await session.execute(

        select(User)
        .filter(User.username == username)
    )

    user = user_query.scalars().first()
    if not user:
        raise HTTPException(
            detail='Current User Not Found',
            status_code=404
        )
    
    repsonse = SUserResponse(
        id = user.id,
        username = user.username
    )

    return repsonse
