
from fastapi import FastAPI
from routers import news_routers
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
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


app.include_router(news_routers.router)

