from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.users.models import User
from app.users.schemas import UserCreate
from typing import List, Optional
import httpx
from app.core.config import settings
from sqlalchemy import func
from app.users.dao import create_user as dao_create_user, get_user as dao_get_user, get_users as dao_get_users, get_random_user as dao_get_random_user
from sqlalchemy.exc import IntegrityError

async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    user = User(**user_data.model_dump())
    return await dao_create_user(db, user)

async def get_user(db: AsyncSession, user_id: int) -> Optional[User]:
    return await dao_get_user(db, user_id)

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 1000) -> List[User]:
    return await dao_get_users(db, skip, limit)

async def get_random_user(db: AsyncSession) -> Optional[User]:
    return await dao_get_random_user(db)

async def fetch_random_users(count: int) -> list:
    async with httpx.AsyncClient() as client:
        response = await client.get(settings.RANDOMUSER_API_URL, params={"results": count})
        response.raise_for_status()
        return (await response.json())["results"]

async def preload_users(db: AsyncSession):
    users = await get_users(db, skip=0, limit=1)
    if not users:
        users_data = await fetch_random_users(1000)
        for user_data in users_data:
            user = UserCreate(
                id=user_data["id"],
                gender=user_data["gender"],
                first_name=user_data["name"]["first"],
                last_name=user_data["name"]["last"],
                phone=user_data["phone"],
                email=user_data["email"],
                location=", ".join([user_data["location"]["country"], user_data["location"]["city"]]),
                picture=user_data["picture"]["thumbnail"]
            )
            try:
                await create_user(db, user)
            except IntegrityError:
                await db.rollback() 