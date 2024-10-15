from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

USER_AND_AUTH_SERVICE_DATABASE_URL = "postgresql+asyncpg://username:password@localhost:5432/AuthUserService"

Base = declarative_base()

engine = create_async_engine(USER_AND_AUTH_SERVICE_DATABASE_URL)

async_session_maker = sessionmaker(bind = engine, class_ = AsyncSession)

async def get_user_service_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()