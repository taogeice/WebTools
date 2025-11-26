# WebTools 后端 API

基于 FastAPI 构建的 WebTools 项目后端服务。

## 项目结构

```
backend/
├── app/
│   ├── api/              # API 路由
│   │   ├── dependencies/ # 依赖注入
│   │   └── router/       # 路由模块
│   ├── core/             # 核心配置
│   │   └── config.py     # 应用配置
│   ├── db/               # 数据库
│   │   └── database.py   # 数据库连接
│   ├── models/           # SQLAlchemy 模型
│   ├── schemas/          # Pydantic 模型
│   ├── services/         # 业务逻辑服务
│   ├── utils/            # 工具函数
│   └── tests/            # 测试文件
├── docs/                 # 文档
├── requirements.txt      # Python 依赖
└── .env.example          # 环境变量示例
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入真实配置
```

### 3. 运行应用

#### 开发模式

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 生产模式

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 端点

### 用户管理

- `GET /api/v1/users/` - 获取用户列表
- `POST /api/v1/users/` - 创建用户
- `GET /api/v1/users/{user_id}` - 获取用户详情
- `PUT /api/v1/users/{user_id}` - 更新用户
- `DELETE /api/v1/users/{user_id}` - 删除用户

### 系统

- `GET /` - 根路径
- `GET /health` - 健康检查

## 开发指南

### 添加新路由

1. 在 `app/api/router/` 下创建路由文件
2. 定义路由函数
3. 在 `app/main.py` 中注册路由

### 添加新模型

1. 在 `app/models/` 下创建模型文件
2. 在 `app/schemas/` 下创建对应的 Pydantic 模型
3. 在 `app/services/` 下添加业务逻辑

### 数据库迁移

使用 Alembic 进行数据库迁移：

```bash
# 初始化
alembic init alembic

# 创建迁移
alembic revision --autogenerate -m "描述"

# 应用迁移
alembic upgrade head
```

## 测试

```bash
pytest app/tests/
```

## 技术栈

- **框架**: FastAPI
- **数据库**: SQLAlchemy + SQLite/PostgreSQL
- **认证**: JWT
- **数据验证**: Pydantic
- **文档**: 自动生成 (OpenAPI/Swagger)

## 许可证

MIT License
