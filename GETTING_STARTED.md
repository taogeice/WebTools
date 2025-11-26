# 黄金价格分析系统 - 快速启动指南

## 📋 系统简介

这是一个完整的黄金价格分析系统，包含：
- **后端**：FastAPI + SQLAlchemy + SQLite
- **数据源**：AKShare（国内） + yfinance（国际）
- **前端**：Vue 3 + Chart.js
- **功能**：实时价格展示、历史数据查询、市场对比分析

## 🚀 快速启动

### 1. 启动后端服务

```bash
# 激活 conda 环境
conda activate fastWeb

# 进入后端目录
cd /home/webCode/pythonWebCode/WebTools/backend

# 安装依赖（首次运行）
pip install -r requirements.txt

# 启动服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

或使用启动脚本：
```bash
cd /home/webCode/pythonWebCode/WebTools/backend
./start.sh
```

后端启动成功后，访问：
- API 文档：http://localhost:8000/docs
- 健康检查：http://localhost:8000/health

### 2. 启动前端服务

```bash
# 进入前端目录
cd /home/webCode/pythonWebCode/WebTools/frontend

# 安装依赖（首次运行）
npm install

# 启动开发服务器
npm run dev
```

前端启动后，访问：http://localhost:5173

## 📊 功能特性

### 价格走势页面
- ✅ 查看国内/国际黄金价格历史数据
- ✅ 自定义日期范围
- ✅ 多种图表类型（折线图、柱状图）
- ✅ 数据统计（最高价、最低价、平均价）
- ✅ 数据同步功能

### 市场对比页面
- ✅ 国内外价格对比图表
- ✅ 统计数据对比表
- ✅ 相关性分析
- ✅ 波动率计算

### 最新价格页面
- ✅ 实时价格展示
- ✅ 自动刷新（每5分钟）
- ✅ 价格对比分析

## 🗂️ API 端点

### 黄金价格 API

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/v1/gold/sync` | 同步数据到数据库 |
| GET | `/api/v1/gold/data/{market_type}` | 获取指定市场数据 |
| GET | `/api/v1/gold/summary/{market_type}` | 获取市场汇总 |
| GET | `/api/v1/gold/comparison` | 比较国内外市场 |
| GET | `/api/v1/gold/latest` | 获取最新价格 |
| GET | `/api/v1/gold/metadata` | 获取数据库元数据 |

### 使用示例

#### 同步数据
```bash
curl -X POST "http://localhost:8000/api/v1/gold/sync" \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
  }'
```

#### 获取数据
```bash
curl "http://localhost:8000/api/v1/gold/data/domestic?start_date=2024-01-01&end_date=2024-01-31"
```

## 📁 项目结构

```
WebTools/
├── backend/                    # 后端
│   ├── app/
│   │   ├── api/router/        # API 路由
│   │   │   ├── gold_price.py  # 黄金价格路由
│   │   │   └── user.py        # 用户路由
│   │   ├── core/              # 核心配置
│   │   │   └── config.py      # 应用配置
│   │   ├── db/                # 数据库
│   │   │   └── database.py    # 数据库连接
│   │   ├── models/            # SQLAlchemy 模型
│   │   │   ├── gold_price.py  # 黄金价格模型
│   │   │   └── user.py        # 用户模型
│   │   ├── schemas/           # Pydantic 模型
│   │   │   ├── gold_price.py  # 黄金价格模式
│   │   │   └── user.py        # 用户模式
│   │   ├── services/          # 业务逻辑
│   │   │   └── gold_price_service.py  # 黄金价格服务
│   │   └── main.py            # 应用入口
│   ├── requirements.txt       # Python 依赖
│   └── start.sh              # 启动脚本
│
├── frontend/                  # 前端
│   ├── src/
│   │   ├── api/
│   │   │   └── gold.js        # 黄金价格API
│   │   ├── components/
│   │   │   ├── GoldPriceChart.vue         # 价格走势图表
│   │   │   ├── GoldPriceComparison.vue    # 市场对比图表
│   │   │   └── LatestPrices.vue           # 最新价格
│   │   ├── App.vue            # 主应用
│   │   └── main.js            # 入口文件
│   ├── package.json           # Node.js 依赖
│   └── vite.config.js         # Vite 配置
│
└── README.md                  # 项目说明
```

## 🛠️ 技术栈

### 后端
- **FastAPI**：现代化、高性能的 Python Web 框架
- **SQLAlchemy**：Python SQL 工具包
- **SQLite**：轻量级数据库
- **AKShare**：金融数据接口库
- **yfinance**：Yahoo Finance API 客户端
- **Pandas**：数据处理库
- **Chart.js**：图表库

### 前端
- **Vue 3**：JavaScript 框架
- **Vite**：构建工具
- **Chart.js**：图表库
- **Axios**：HTTP 客户端
- **date-fns**：日期处理库

## 📝 注意事项

1. **首次运行**：首次启动时，系统会自动创建 SQLite 数据库文件 `backend/app.db`

2. **数据同步**：如果数据库中没有数据，请先使用"同步数据"按钮从 API 获取数据

3. **网络问题**：如果 API 数据获取失败，系统会自动使用模拟数据

4. **CORS 配置**：已配置允许前端端口（3000, 5173, 8080）

5. **自动刷新**：最新价格页面会自动每5分钟刷新一次

## 🔧 常见问题

### Q: 前端无法访问后端 API
A: 检查：
- 后端是否在 8000 端口启动
- CORS 配置是否正确
- 防火墙是否阻止

### Q: 图表不显示
A: 检查：
- 是否已同步数据
- 控制台是否有错误
- Chart.js 是否正确加载

### Q: 数据获取失败
A: 正常现象，系统会使用模拟数据。可稍后重试同步。

## 📄 许可证

MIT License
