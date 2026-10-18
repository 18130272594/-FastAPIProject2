
from fastapi import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from CRUD import users_crud
from models.users_model import User
from schemas.users import UserRequest, UserAuthRequest, UserInfoResponse

from config.ormbase import get_database
from utils.AUTH import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["users"])
@router.post("/register" )
async def register_user(user_data: UserRequest,db:AsyncSession=Depends(get_database)):
    user=await users_crud.get_username(db, user_data.username)
    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    user_new=await users_crud.create_user(db,user_data)
    new_token=await users_crud.create_token(db,user_new.id)
    re_data=UserAuthRequest(token=new_token,user_info=UserInfoResponse.model_validate(user_new))
    return success_response(message="注册成功",data=re_data)
    # return {
    #   "code": 200,
    #   "message": "注册成功",
    #   "data": {
    #     "token": token,
    #     "userInfo": {
    #       "id": user_new.id,
    #       "username": user_new.username,
    #       "bio": user_new.bio,
    #       "avatar": user_new.avatar
    #     }   # avatar: 用户头像
    #  }
    # }
@router.post("/login")
async def login_user(user_data: UserRequest,db:AsyncSession=Depends(get_database)):
     user= await  users_crud.query_users(db,user_data.username,user_data.password)
     if not user:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
     token = await users_crud.create_token(db, user.id)
     response_data = UserAuthRequest(token=token, user_info=UserInfoResponse.model_validate(user))
     return success_response(message="登录成功", data=response_data)
@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    return success_response(message = "获取用户信息成功", data = UserInfoResponse.model_validate(user))


