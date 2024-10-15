from sqlalchemy.ext.asyncio import AsyncSession
from src.core.databse import get_user_service_session
from .service import UserService
from fastapi import APIRouter, Form, Depends

user_service_router = APIRouter(tags=['User Service'])


@user_service_router.post("/user-service/sign-up/")
async def sign_up(session: AsyncSession = Depends(get_user_service_session), username: str = Form(...), password: str = Form(...)):
    serivice = UserService(session=session)
    return await serivice.sign_up(username=username, password=password)


@user_service_router.delete("/delete-user/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_user_service_session)):
    service = UserService(session=session)
    return await service.delete_user(user_id=user_id)
    