

from fastapi import APIRouter, Depends, Query,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from CRUD import  news_crud
from config.ormbase import get_database

router = APIRouter(prefix="/api/news", tags=["news"])


@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession=Depends(get_database)):
    categories=await news_crud.get_categories(db,skip, limit)
    return {
        "code": 200,
        "msg":"获取分类成功",
        "data":categories
    }
@router.get("/list")
async def list_categories(
        category_id: int=Query(...,alias="categoryId"),
        page: int = 1,
        page_size: int =Query(100,alias="pageSize",le=100),
        db: AsyncSession=Depends(get_database)
):
    offset=(page-1)*page_size
    news_list= await news_crud.get_news_list(db,category_id,offset,page_size)
    total=await news_crud.get_news_total(db,category_id)
    has_more=offset+len(news_list)<total
    return {
        "code": 200,
        "message":"获取列表成功",
        "data":{
            "list":news_list,
            "total":total,
            "hasMore":has_more
        }
    }
@router.get("/detail")
async def detail(news_id: int=Query(...,alias="id"), db: AsyncSession=Depends(get_database)):
    #获取新闻详细，浏览量，相关推荐
   news_detail = await news_crud.get_news_detail(db,news_id)
   if not news_detail:
       raise   HTTPException(status_code=404,detail="新闻不存在")
   await news_crud.get_news_views(db,news_id)
   relate_news=await news_crud.news_crud_related(db,news_detail.id,news_detail.category_id)
   return {
     "code": 200,
     "message": "success",
     "data": {
         "id": news_detail.id,
         "title": news_detail.title,
         "content": news_detail.content,
         "image": news_detail.image,
         "author": news_detail.author,
         "publishTime": news_detail.publish_time,
         "categoryId": news_detail.category_id,
         "views": news_detail.views,
         "relatedNews": relate_news
     }
 }