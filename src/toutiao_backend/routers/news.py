from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from toutiao_backend.common.page_result import PageResult
from toutiao_backend.config.db_conf import get_db

from ..common.result import Result
from ..crud import news

# 创建 APIRouter 实例
router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/categories", response_model=Result)
async def get_categories(
    db: AsyncSession = Depends(get_db), skip: int = 0, limit: int = 100
):
    result = await news.get_category(db, skip, limit)
    return Result.success(result)


@router.get("/list",response_model=PageResult)
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

    return PageResult.page(
        list_data=news_list,
        total=total,
        has_more=has_more
    )


@router.get("/detail", response_model=Result)
async def get_news_detail(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    new_detail = await news.get_news_detail(db, id)
    if not new_detail:
        raise HTTPException(status_code=404,detail="此新闻不存在")
    await news.increase_news_views(db, id)
    # 新闻详情-相关推荐
    related_news = await news.get_related_news(
        db,
        new_detail.id,
        new_detail.category_id
    )
 
    data = {
        "id": new_detail.id,
        "title": new_detail.title,
        "description": new_detail.description,
        "content": new_detail.content,
        "image": new_detail.image,
        "author": new_detail.author,
        "publishTime": new_detail.publish_time,
        "categoryId": new_detail.category_id,
        "views": new_detail.views + 1,
        "relatedNews": related_news
    }
 
    return Result.success(data)
