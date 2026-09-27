from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import news, users

app = FastAPI()

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    # allow_origins=[origins],      # 生成环境
    allow_origins=["*"],  # 允许访问的源
    allow_credentials=True,  # 允许携带 Cookie
    allow_methods=["*"],  # 允许所有请求方法
    allow_headers=["*"],  # 允许所有请求头
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# 挂载路由/注册路由
app.include_router(news.router)
app.include_router(users.router)
app.include_router(users.compat_router)