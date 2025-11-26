"""
用户路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.dependencies.deps import get_db
from app.services.user import user_service
from app.schemas.user import User, UserCreate, UserUpdate

router = APIRouter()


@router.get("/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取用户列表"""
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=User)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """创建用户"""
    db_user = user_service.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return user_service.create_user(db=db, user=user)


@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    """获取用户详情"""
    db_user = user_service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user


@router.put("/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """更新用户"""
    db_user = user_service.update_user(db=db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """删除用户"""
    success = user_service.delete_user(db=db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"message": "用户删除成功"}
