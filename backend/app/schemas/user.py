"""
用户 Pydantic 模型
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """用户基础模型"""
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True


class UserCreate(UserBase):
    """创建用户模型"""
    password: str


class UserUpdate(BaseModel):
    """更新用户模型"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase):
    """用户响应模型"""
    id: int
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class UserInDB(User):
    """用户数据库模型"""
    hashed_password: str
