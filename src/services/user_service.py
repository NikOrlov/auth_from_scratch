import logging
from functools import lru_cache
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from schemas.entity import User
from db.postgres import get_session
from models.user import UserCreate


class UserService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create_user(self, user: UserCreate) -> User:
        user = User(**user.dict())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_user_by_login(self, login: str) -> User | None:
        try:
            result = await self.db.execute(select(User).where(User.login == login))
            return result.scalars().first()
        except SQLAlchemyError as e:
            logging.error(e)


@lru_cache()
def get_user_service(
        db: AsyncSession = Depends(get_session),
) -> UserService:
    return UserService(db)
