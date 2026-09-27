
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
#数据库ULR
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/news_app?charset=utf8mb4"
#创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,
    pool_size=10,
    max_overflow=20,
)
#创建异步会话
AsyncSession_mo = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
#依赖项。获取数据库会话
async def get_database():
    async with AsyncSession_mo() as session:
        try:
            yield session
            await session.commit()#
        except Exception:
           await session.rollback()
           raise
        finally:
            await session.close()