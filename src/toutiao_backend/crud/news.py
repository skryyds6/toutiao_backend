

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from toutiao_backend.models.news import Category

from ..models.news import News


async def get_category(db:AsyncSession,skip:int,limit:int):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_news_list(db:AsyncSession,category_id:int,skip:int,limit:int):
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_news_total(db:AsyncSession,category_id:int):
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()

async def get_news_detail(db:AsyncSession,new_id:int):
    stmt =  select(News).where(News.id == new_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()