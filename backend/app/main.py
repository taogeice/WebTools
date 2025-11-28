"""
FastAPI 主应用入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import engine, Base

# 导入所有模型，以确保它们被注册到 Base.metadata
from app.models import gold_price  # noqa
from app.models import user  # noqa

# 创建所有数据库表
Base.metadata.create_all(bind=engine)

# 应用实例
app = FastAPI(
    title=settings.APP_NAME,
    description="WebTools 项目后端 API",
    version=settings.APP_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 路由注册
from app.api.router.user import router as user_router
from app.api.router.gold_price import router as gold_price_router

# 注册用户路由
app.include_router(user_router, prefix=settings.API_V1_STR + "/users", tags=["users"])

# 注册黄金价格路由
app.include_router(gold_price_router, prefix=settings.API_V1_STR + "/gold", tags=["gold"])

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# 根路径
@app.get("/")
async def root():
    return {"message": "欢迎使用 WebTools API"}
