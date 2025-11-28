# WebTools 后端 API

基于 FastAPI 构建的小工具箱后端服务，提供完整的 RESTful API 和数据管理功能，支持多种实用工具和数据分析。

## 项目概述

WebTools 是一个现代化的工具箱平台，后端采用 FastAPI 框架，支持：

- 🏦 **双数据源支持**：AKShare（国内金融数据）和 yfinance（国际金融数据）
- 📊 **实时数据处理**：自动获取、处理和存储黄金价格数据
- 🔒 **安全认证**：基于 JWT 的用户认证和授权系统
- 📈 **数据分析**：支持历史数据查询、趋势分析和市场对比
- 🚀 **高性能**：异步处理，支持高并发访问
- 📚 **自动文档**：自动生成 OpenAPI/Swagger 文档

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI 应用入口和路由注册
│   ├── api/                    # API 路由层
│   │   ├── __init__.py
│   │   ├── dependencies.py     # API 依赖注入
│   │   └── router/             # 路由模块
│   │       ├── __init__.py
│   │       ├── gold.py         # 黄金价格相关路由
│   │       ├── users.py        # 用户管理路由
│   │       └── system.py       # 系统监控路由
│   ├── core/                   # 核心配置
│   │   ├── __init__.py
│   │   ├── config.py           # 应用配置管理
│   │   └── security.py         # 安全相关配置
│   ├── db/                     # 数据库层
│   │   ├── __init__.py
│   │   ├── database.py         # SQLAlchemy 数据库连接
│   │   └── session.py          # 数据库会话管理
│   ├── models/                 # SQLAlchemy ORM 模型
│   │   ├── __init__.py
│   │   ├── user.py             # 用户模型
│   │   └── gold_price.py       # 黄金价格模型
│   ├── schemas/                # Pydantic 数据验证模型
│   │   ├── __init__.py
│   │   ├── user.py             # 用户数据模式
│   │   └── gold_price.py       # 黄金价格数据模式
│   ├── services/               # 业务逻辑服务层
│   │   ├── __init__.py
│   │   ├── auth_service.py     # 认证服务
│   │   ├── gold_service.py     # 黄金价格服务
│   │   └── data_sync_service.py # 数据同步服务
│   ├── utils/                  # 工具函数
│   │   ├── __init__.py
│   │   ├── akshare_client.py   # AKShare 数据客户端
│   │   └── yfinance_client.py  # yfinance 数据客户端
│   └── tests/                  # 测试文件
│       ├── __init__.py
│       ├── conftest.py         # pytest 配置
│       ├── test_auth.py        # 认证测试
│       └── test_gold.py        # 黄金价格测试
├── alembic/                    # 数据库迁移
│   ├── versions/               # 迁移版本文件
│   ├── env.py                  # Alembic 环境配置
│   └── script.py.mako          # 迁移脚本模板
├── docs/                       # 项目文档
├── requirements.txt             # Python 依赖列表
├── .env.example               # 环境变量示例
├── alembic.ini                # Alembic 配置文件
├── pytest.ini                # pytest 配置文件
└── start.sh                   # 启动脚本
```

## 快速开始

### 环境要求

- Python 3.8+
- SQLAlchemy 1.4+
- PostgreSQL (生产环境) / SQLite (开发环境)

### 1. 克隆项目并进入后端目录

```bash
cd backend
```

### 2. 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，配置数据库连接等信息
# 重要：生产环境必须修改 SECRET_KEY
```

### 5. 初始化数据库

```bash
# 创建数据库表
alembic upgrade head

# 或者创建初始迁移
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

### 6. 运行应用

#### 开发模式（推荐）

```bash
# 使用 uvicorn 自动重载
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或使用启动脚本
chmod +x start.sh
./start.sh
```

#### 生产模式

```bash
# 无重载模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# 使用 Gunicorn (推荐生产环境)
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### 7. 访问 API 文档

启动成功后，访问以下地址：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json
- **健康检查**: http://localhost:8000/health

## API 端点

### 认证管理

- `POST /api/v1/auth/login` - 用户登录
- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/refresh` - 刷新访问令牌
- `POST /api/v1/auth/logout` - 用户登出

### 用户管理

- `GET /api/v1/users/` - 获取用户列表（需管理员权限）
- `GET /api/v1/users/me` - 获取当前用户信息
- `POST /api/v1/users/` - 创建用户（管理员）
- `GET /api/v1/users/{user_id}` - 获取指定用户详情
- `PUT /api/v1/users/{user_id}` - 更新用户信息
- `DELETE /api/v1/users/{user_id}` - 删除用户（管理员）

### 黄金价格数据

- `GET /api/v1/gold/` - 获取黄金价格列表
- `GET /api/v1/gold/latest` - 获取最新黄金价格
- `GET /api/v1/gold/market/{market}` - 按市场获取价格
- `GET /api/v1/gold/range` - 获取指定日期范围的数据
- `GET /api/v1/gold/compare` - 市场价格对比分析
- `POST /api/v1/gold/sync` - 手动同步数据（管理员）

### 数据统计

- `GET /api/v1/stats/summary` - 数据概览统计
- `GET /api/v1/stats/market/{market}` - 特定市场统计
- `GET /api/v1/stats/trends` - 价格趋势分析

### 系统

- `GET /` - API 根路径，返回基本信息
- `GET /health` - 健康检查
- `GET /version` - 获取应用版本信息
- `GET /api/v1/system/status` - 系统状态检查

#### 示例 API 调用

```bash
# 获取最新黄金价格
curl -X GET "http://localhost:8000/api/v1/gold/latest"

# 按日期范围查询
curl -X GET "http://localhost:8000/api/v1/gold/range?start_date=2024-01-01&end_date=2024-01-31"

# 用户登录
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

## 开发指南

### 代码规范

- 遵循 PEP 8 Python 编码规范
- 使用类型注解增强代码可读性
- 所有 API 端点必须有完整的文档字符串
- 使用 Pydantic 进行数据验证
- 遵循 RESTful API 设计原则

### 添加新功能模块

#### 1. 创建数据模型

在 `app/models/` 中创建 SQLAlchemy 模型：

```python
# app/models/example.py
from sqlalchemy import Column, Integer, String, DateTime
from app.db.database import Base

class Example(Base):
    __tablename__ = "examples"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### 2. 创建 Pydantic 模式

在 `app/schemas/` 中创建数据验证模式：

```python
# app/schemas/example.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ExampleBase(BaseModel):
    name: str

class ExampleCreate(ExampleBase):
    pass

class ExampleUpdate(BaseModel):
    name: Optional[str] = None

class Example(ExampleBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
```

#### 3. 创建业务服务

在 `app/services/` 中实现业务逻辑：

```python
# app/services/example_service.py
from sqlalchemy.orm import Session
from app.models.example import Example
from app.schemas.example import ExampleCreate

class ExampleService:
    def get_example(self, db: Session, example_id: int):
        return db.query(Example).filter(Example.id == example_id).first()

    def get_examples(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(Example).offset(skip).limit(limit).all()

    def create_example(self, db: Session, example: ExampleCreate):
        db_example = Example(**example.dict())
        db.add(db_example)
        db.commit()
        db.refresh(db_example)
        return db_example
```

#### 4. 创建 API 路由

在 `app/api/router/` 中创建路由：

```python
# app/api/router/example.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.services.example_service import ExampleService
from app.schemas.example import Example, ExampleCreate

router = APIRouter()
example_service = ExampleService()

@router.post("/examples/", response_model=Example)
def create_example(example: ExampleCreate, db: Session = Depends(get_db)):
    return example_service.create_example(db=db, example=example)

@router.get("/examples/{example_id}", response_model=Example)
def get_example(example_id: int, db: Session = Depends(get_db)):
    db_example = example_service.get_example(db, example_id)
    if db_example is None:
        raise HTTPException(status_code=404, detail="Example not found")
    return db_example
```

#### 5. 注册路由

在 `app/main.py` 中注册新路由：

```python
from app.api.router import example

app.include_router(example.router, prefix="/api/v1", tags=["examples"])
```

### 数据库迁移

使用 Alembic 进行数据库版本管理：

```bash
# 初始化 Alembic（首次使用）
alembic init alembic

# 创建新的迁移文件
alembic revision --autogenerate -m "添加新表或字段"

# 手动创建迁移文件
alembic revision -m "自定义迁移"

# 查看迁移历史
alembic history

# 应用迁移（升级到最新版本）
alembic upgrade head

# 应用到指定版本
alembic upgrade <revision_id>

# 回滚迁移
alembic downgrade -1
alembic downgrade base

# 查看当前版本
alembic current
```

### 环境变量配置

在 `.env` 文件中配置以下环境变量：

```bash
# 应用配置
APP_NAME=WebTools API
APP_VERSION=1.0.0
DEBUG=True
SECRET_KEY=your-secret-key-here  # 生产环境必须修改

# 数据库配置
DATABASE_URL=sqlite:///./webtools.db
# PostgreSQL: DATABASE_URL=postgresql://user:password@localhost/webtools

# CORS 配置
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]

# JWT 配置
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 数据源配置
AKSHARE_ENABLED=True
YFINANCE_ENABLED=True

# 日志配置
LOG_LEVEL=INFO
```

## 测试

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest app/tests/test_auth.py

# 运行测试并显示覆盖率
pytest --cov=app --cov-report=html

# 详细输出
pytest -v

# 运行特定标记的测试
pytest -m "unit"
pytest -m "integration"
```

### 测试配置

在 `pytest.ini` 中配置测试参数：

```ini
[tool:pytest]
testpaths = app/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### 示例测试

```python
# app/tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_login():
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
```

## 部署

### Docker 部署

创建 `Dockerfile`：

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

构建和运行：

```bash
# 构建镜像
docker build -t webtools-backend .

# 运行容器
docker run -p 8000:8000 -e DATABASE_URL=sqlite:///./webtools.db webtools-backend
```

### 使用 Docker Compose

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/webtools
    depends_on:
      - db
    volumes:
      - ./app:/app/app

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=webtools
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  frontend:
    build: ../frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
```

### 生产环境注意事项

1. **安全配置**：

   - 修改默认的 `SECRET_KEY`
   - 使用 HTTPS 协议
   - 配置防火墙规则
2. **性能优化**：

   - 使用 Gunicorn + Uvicorn workers
   - 配置数据库连接池
   - 启用 Redis 缓存
3. **监控和日志**：

   - 配置结构化日志
   - 设置监控指标收集
   - 配置错误报告
4. **数据库**：

   - 使用 PostgreSQL 替代 SQLite
   - 配置数据库备份策略
   - 设置读写分离（如需要）

## 技术栈

- **Web 框架**: FastAPI 0.104+
- **ORM**: SQLAlchemy 2.0+
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **认证**: JWT (JSON Web Tokens)
- **数据验证**: Pydantic V2
- **文档生成**: OpenAPI 3.0 / Swagger UI
- **测试框架**: pytest
- **代码质量**: Black, isort, flake8
- **数据源**: AKShare, yfinance
- **任务队列**: Celery + Redis (可选)
- **部署**: Docker, Gunicorn, Nginx

## 常见问题

### Q: 如何重置数据库？

```bash
# 删除数据库文件
rm webtools.db

# 重新运行迁移
alembic upgrade head
```

### Q: 如何添加新的数据源？

1. 在 `app/utils/` 中创建新的客户端
2. 在 `app/services/` 中集成数据源服务
3. 更新配置文件和环境变量

### Q: 如何处理数据同步失败？

- 检查网络连接
- 验证数据源 API 配额
- 查看应用日志获取详细错误信息

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情
