from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db

async def get_db_session(db: AsyncSession = Depends(get_db)):
    return db 