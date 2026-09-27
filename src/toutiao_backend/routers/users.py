from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from toutiao_backend.common.result import Result
from toutiao_backend.config.db_conf import get_db
from toutiao_backend.utils.response import success_response

from ..crud import users
from ..schemas.users import UserAuthResponse, UserInfoResponse, UserRequest

router = APIRouter(prefix="/api/users",tags=["users"])
compat_router = APIRouter(prefix="/api/user", tags=["users"])

@compat_router.post("/register", include_in_schema=False)
@router.post("/register")
async def register(user_data:UserRequest,db:AsyncSession = Depends(get_db)):

    db_user = await users.get_user_by_username(db,user_data.username)
    if db_user:
        return Result.error("用户已存在",400)

    # 新增用户
    user = await users.create_user(db, user_data)
 # 生成 Token
    token = await users.create_token(db, user.id)


    ## 构建响应数据：token + 用户信息
    # model_validate: 将 ORM 模型对象转换为 Pydantic 响应模型
    response_data = UserAuthResponse(token=token, userInfo=UserInfoResponse.model_validate(user))
    return success_response(data=response_data)
