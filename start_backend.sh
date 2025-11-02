#!/bin/bash

# AI Trading Analyzer - Backend Start Script
# 后端服务器启动脚本

echo "================================================"
echo "🚀 AI Trading Analyzer - Backend Server"
echo "================================================"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ 错误：找不到 .env 文件"
    echo "请先创建 .env 文件并添加 OPENAI_API_KEY"
    echo ""
    echo "示例："
    echo "OPENAI_API_KEY=your_key_here"
    echo "PORT=8000"
    echo "ALLOWED_ORIGINS=http://localhost:3000"
    echo ""
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到 Python 3"
    echo "请先安装 Python 3.8 或更高版本"
    exit 1
fi

echo "✅ 检测到 Python: $(python3 --version)"
echo ""

# Check if dependencies are installed
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "⚠️  警告：未检测到依赖包"
    echo "正在安装依赖..."
    pip3 install -r requirements.txt
    echo ""
fi

echo "🔧 启动后端服务器..."
echo "📍 地址: http://localhost:8000"
echo "📋 API 文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "================================================"
echo ""

# Start the server
python3 server.py

