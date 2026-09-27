from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from toutiao_backend.common.result import Result
from toutiao_backend.config.db_conf import get_db
from ..schemas.users import UserRequest
from ..crud import users
router = APIRouter(prefix="/api/users",tags=["users"])

@router.post("/register")
async def register(user_data:UserRequest,db:AsyncSession = Depends(get_db)):

    db_user = await users.get_user_by_username(db,user_data.username)
    if db_user:
        return Result.error("用户已存在",400)

    # 新增用户
    user = await users.create_user(db, user_data)
 # 生成 Token
    token = await users.create_token(db, user.id)
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": token,
            "userInfo": {
                "id": user.id,
                "username": user_data.username,
                "bio": user.bio,
                "avatar": user.avatar
            }
        }
    }
