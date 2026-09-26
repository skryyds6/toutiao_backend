from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from toutiao_backend.config.db_conf import get_db

from ..crud import news

# 创建 APIRouter 实例
router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/categories")
async def get_categories(
    db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100
):
    result = await news.get_category(db, skip, limit)
    return {"code": 200, "message": "获取新闻分类成功", "data": result}


@router.get("/list")
async def get_news_list(
    db: AsyncSession = Depends(get_db),
    category_id: int = Query(..., alias="categoryID"),
    page: int = 1,
    page_size: int = Query(10, le=100, alias="pageSize"),
):
    offset: int = (page - 1) * page_size
    news_list = await news.get_news_list(db, category_id, offset, page_size)
    total = await news.get_news_total(db, category_id)
    has_more = (offset + len(news_list)) < total
    return {
        "code": 200,
        "message": "获取新闻列表成功",
        "data": {"list": news_list, "total": total, "hasMore":has_more},
    }

@router.get("/datail")
async def get_news_detail(new_id:int,db = Depends(get_db)):
    new_detail = await news.get_news_detail(db,new_id)
    if not new_detail:
        raise HTTPException(status_code=404,detail="此新闻不存在")
    return new_detail