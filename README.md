# WebTools - 黄金价格分析系统

一个基于 Vue 3 + FastAPI 的现代化黄金价格分析平台，提供实时价格监控、历史数据分析和市场对比功能。

## 🌟 项目特性

- **实时价格监控**：支持国内外黄金价格实时更新
- **历史数据分析**：自定义日期范围的价格走势图表
- **市场对比分析**：国内外市场价格对比和相关性分析
- **响应式设计**：适配多种设备和屏幕尺寸
- **双数据源**：集成 AKShare（国内）和 yfinance（国际）金融数据

## 🏗️ 系统架构

### 后端 (FastAPI)

- **技术栈**：FastAPI + SQLAlchemy + SQLite/PostgreSQL
- **主要功能**：
  - RESTful API 服务
  - 金融数据获取和处理
  - 数据持久化和缓存
  - 用户认证和授权
  - 自动生成 API 文档

### 前端 (Vue 3)

- **技术栈**：Vue 3 + Vite + Chart.js + Axios
- **主要功能**：
  - 交互式数据可视化
  - 实时价格展示
  - 历史数据图表分析
  - 市场对比界面
  - 响应式用户体验

## 🚀 快速开始

### 环境要求

- **后端**：Python 3.8+, Node.js 16+
- **前端**：Node.js 16+, npm 8+

### 启动后端服务

```bash
# 进入后端目录
cd backend

# 安装 Python 依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端启动后访问：

- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

### 启动前端服务

```bash
# 进入前端目录
cd frontend

# 安装 Node.js 依赖
npm install

# 启动开发服务器
npm run dev
```

前端启动后访问：http://localhost:5173

## 📊 功能模块

### 📈 价格走势分析

- 查看国内/国际黄金价格历史数据
- 自定义日期范围筛选
- 多种图表类型（折线图、柱状图）
- 数据统计（最高价、最低价、平均价）

### 🔍 市场对比

- 国内外价格对比图表
- 统计数据对比表
- 相关性分析
- 波动率计算

### ⚡ 实时价格

- 实时价格展示
- 自动刷新（每5分钟）
- 价格变化趋势分析

## 🛠️ 开发指南

### 后端开发

```bash
cd backend
# 安装依赖
pip install -r requirements.txt
# 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# 运行测试
pytest
```

### 前端开发

```bash
cd frontend
# 安装依赖
npm install
# 启动开发服务器
npm run dev
# 构建生产版本
npm run build
```

## 📁 项目结构

```
WebTools/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── api/               # API 路由
│   │   ├── core/              # 核心配置
│   │   ├── db/                # 数据库连接
│   │   ├── models/            # SQLAlchemy 模型
│   │   ├── schemas/           # Pydantic 模式
│   │   ├── services/          # 业务逻辑
│   │   └── main.py            # 应用入口
│   ├── requirements.txt       # Python 依赖
│   └── start.sh              # 启动脚本
│
├── frontend/                  # Vue 3 前端
│   ├── src/
│   │   ├── api/               # API 调用
│   │   ├── components/        # Vue 组件
│   │   ├── App.vue           # 主应用
│   │   └── main.js           # 入口文件
│   ├── package.json           # Node.js 依赖
│   └── vite.config.js         # Vite 配置
│
├── CLAUDE.md                   # Claude Code 指南
├── GETTING_STARTED.md          # 详细启动指南
└── README.md                   # 项目说明
```

## 🔧 技术栈

### 后端技术

- **FastAPI**：现代化、高性能的 Python Web 框架
- **SQLAlchemy**：Python SQL 工具包和 ORM
- **Pydantic**：数据验证和序列化
- **AKShare**：国内金融数据接口
- **yfinance**：Yahoo Finance API 客户端
- **Pandas**：数据处理和分析
- **Uvicorn**：ASGI 服务器

### 前端技术

- **Vue 3**：渐进式 JavaScript 框架
- **Vite**：下一代前端构建工具
- **Chart.js**：灵活的图表库
- **Axios**：Promise 基础的 HTTP 客户端
- **date-fns**：现代日期工具库

## 📝 API 文档

启动后端服务后，访问 http://localhost:8000/docs 查看完整的 API 文档。

### 主要端点

- `GET /api/v1/gold/latest` - 获取最新价格
- `GET /api/v1/gold/data/{market_type}` - 获取历史数据
- `POST /api/v1/gold/sync` - 同步数据到数据库
- `GET /api/v1/gold/comparison` - 市场对比数据

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送到分支：`git push origin feature/AmazingFeature`
5. 提交 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。
