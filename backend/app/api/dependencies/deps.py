"""
API 依赖注入
"""
from typing import Generator
from sqlalchemy.orm import Session
from app.db.database import SessionLocal


def get_db() -> Generator:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
