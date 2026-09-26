
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.users import User
from ..schemas.users import UserRequest
from ..utils import security

async def get_user_by_username(db:AsyncSession,username: str):
    stmt =  select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def create_user(db:AsyncSession,user_data:UserRequest):

    # 密码加密
    hashed_password = security.get_hash_password(user_data.password)
    user = User(username=user_data.username, password=hashed_password)
 

    db.add(user)
    await db.commit()
    await db.refresh(user)  #刷新,从数据库读最新的
    return user