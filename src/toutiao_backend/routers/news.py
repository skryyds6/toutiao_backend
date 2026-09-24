
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from toutiao_backend.config.db_conf import get_db

from ..crud import news

# 创建 APIRouter 实例                                      
router = APIRouter(prefix="/api/news", tags=["news"])
 
@router.get("/categories")
async def get_categories(db:AsyncSession = Depends(get_db),skip:int = 0, limit:int = 100):  # noqa: B008
    result = await news.get_category(db,skip,limit)
    return{
        "code":200,
        "message":"获取新闻分类成功",
        "data": result
    }