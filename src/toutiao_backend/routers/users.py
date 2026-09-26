from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from toutiao_backend.config.db_conf import get_db
from ..schemas.users import User

router = APIRouter(prefix="/api/users",tags=["users"])

@router.post("/register")
async def register(user:User,db:AsyncSession = Depends(get_db)):
    return {
            "code": 200,
            "message": "注册成功",
            "data": {
                "token": "用户访问令牌",
                "userInfo": {
                    "id": 1,
                    "username": user.username,
                    "bio": "这个人很懒，什么都没留下",
                    "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
                }
            }
        }
