from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.services.user_service.models import User
from src.services.user_service.hash import Hash
from fastapi import HTTPException, Form


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def sign_up(self, username: str = Form(...), password: str = Form(...)):

        exist_username_query = await self.session.execute(
            select(User).filter(User.username == username)
        )

        exist_username = exist_username_query.scalars().first()
        if exist_username:
            raise HTTPException(
                detail=f"{username} This username all ready using", status_code=403
            )

        hashing_password = Hash.bcrypt(password=password)

        user = User(username=username, password=hashing_password)

        self.session.add(user)
        await self.session.commit()

        return {"Detail": "Sign Up Succsesfully"}


    async def delete_user(self, user_id: int):

        user_query = await self.session.execute(
            
            select(User)
            .filter(User.id == user_id)

        )

        user = user_query.scalars().first()
        if not user:
            raise HTTPException(
                detail = "Not Found",
                status_code=404
            )
        
        await self.session.delete(user)
        await self.session.commit()
        