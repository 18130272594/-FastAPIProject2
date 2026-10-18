from pydantic import Field, ConfigDict
from typing import Optional
from  pydantic import BaseModel


class UserRequest(BaseModel):
    username: str
    password: str

class UserInfoBase(BaseModel):
        """
        ⽤户信息基础数据模型
        """
        nickname: Optional[str] = Field(None, max_length=50, description="昵称")
        avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
        gender: Optional[str] = Field(None, max_length=10, description="性别")
        bio: Optional[str] = Field(None, max_length=500, description="个⼈简介")
class UserInfoResponse(UserInfoBase):
      id: int
      username:str
      model_config = ConfigDict(

          from_attributes=True

      )

class  UserAuthRequest(BaseModel):

    token: str
    user_info:UserInfoResponse=Field(...,alias="userInfo")
    model_config=ConfigDict(
        populate_by_name=True,
        from_attributes=True

    )



