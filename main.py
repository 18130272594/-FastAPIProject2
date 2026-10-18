
from fastapi import FastAPI
from routers import news_routers,users_routers
from fastapi.middleware.cors import CORSMiddleware

from utils.EXCEPTION_HANDLER import register_exception_handlers

app = FastAPI()
#注册异常处理器
register_exception_handlers(app)
#中间件解决跨域问题
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,#允许携带COOKIE
    allow_methods=["*"],#允许的方法
    allow_headers=["*"],#允许的请求头
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

#注册路由
app.include_router(news_routers.router)
app.include_router(users_routers.router)

