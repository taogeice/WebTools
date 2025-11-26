#!/bin/bash
# FastAPI 开发启动脚本

# 激活 Conda 环境
echo "激活 Conda 环境: fastWeb"
conda activate fastWeb


# 运行应用
echo "启动 FastAPI 开发服务器..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
