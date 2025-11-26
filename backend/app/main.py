"""
FastAPI 主应用入口
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

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
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 路由注册
from app.api.router.user import router as user_router

# 注册用户路由
app.include_router(user_router, prefix=settings.API_V1_STR + "/users", tags=["users"])

# 健康检查端点
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# 根路径
@app.get("/")
async def root():
    return {"message": "欢迎使用 WebTools API"}
