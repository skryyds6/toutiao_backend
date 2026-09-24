
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from toutiao_backend.models.news import Category


async def get_category(db:AsyncSession,skip:int,limit:int):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()