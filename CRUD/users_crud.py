import uuid
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.users_model import User, UserToken
from schemas.users import UserRequest
from utils import security


async def get_username(db: AsyncSession, username: str):
    query=select(User).where(User.username==username)
    result=await db.execute(query)
    return result.scalar_one_or_none()
async def create_user(db: AsyncSession, userdata: UserRequest):
     has_pad=security.has_password(userdata.password)
     user=User(username=userdata.username, password=has_pad)
     db.add(user)
     await db.commit()
     await db.refresh(user)
     return user
async def create_token(db,user_id: int):
    #生成，时间
    token=str(uuid.uuid4())
    expires_at= datetime.now() + timedelta(days=7)
    query=select(UserToken).where( UserToken.user_id==user_id)
    result=await db.execute(query)
    user_token=result.scalar_one_or_none()
    if user_token:
        user_token.token=token
        user_token.expires_at=expires_at
        await db.commit()
        await db.refresh(user_token)
    else:
        user_token=UserToken(user_id=user_id,token=token,expires_at=expires_at)
        db.add(user_token)
        await db.commit()
    return token
async def query_users(db: AsyncSession, username,password):
      ruser= await get_username(db, username)
      if not ruser:
          return None
      if not security.verify_password(password, ruser.password):
          return None
      return ruser
async def query_user_token(db,token:str):
    query= select(UserToken).where(UserToken.token==token)
    result=await db.execute(query)
    db_token=result.scalar_one_or_none()

    if not db_token or db_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

