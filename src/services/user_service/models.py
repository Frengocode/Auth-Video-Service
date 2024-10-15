from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
from src.core.databse import Base
from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, index = True,  primary_key  = True)
    username: Mapped[str] = mapped_column(String, nullable = False)
    password: Mapped[str] = mapped_column(String, nullable = False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default = datetime.utcnow())