#!/bin/bash
# FastAPI 开发启动脚本

# 激活 Conda 环境
echo "激活 Conda 环境: fastWeb"
conda activate fastWeb

# 安装/更新依赖
echo "安装依赖..."
pip install -r requirements.txt

# 运行应用
echo "启动 FastAPI 开发服务器..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
