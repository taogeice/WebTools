"""
应用配置
"""
import os
from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    """应用设置"""
    # 应用基础配置
    APP_NAME: str = "WebTools API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # 数据库配置
    DATABASE_URL: str = "sqlite:///./app.db"
    # PostgreSQL 示例: postgresql://user:password@localhost/dbname

    # API 配置
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

    # CORS 配置
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    # JWT 配置
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 天

    class Config:
        env_file = ".env"
        case_sensitive = True


# 创建设置实例
settings = Settings()
