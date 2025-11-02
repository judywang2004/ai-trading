#!/bin/bash

# AI Trading Analyzer - Frontend Start Script
# 前端服务器启动脚本

echo "================================================"
echo "🎨 AI Trading Analyzer - Frontend Server"
echo "================================================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ 错误：未找到 Node.js"
    echo "请先安装 Node.js 16 或更高版本"
    exit 1
fi

echo "✅ 检测到 Node.js: $(node --version)"
echo "✅ 检测到 npm: $(npm --version)"
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "⚠️  警告：未检测到 node_modules"
    echo "正在安装依赖..."
    npm install
    echo ""
fi

echo "🔧 启动前端开发服务器..."
echo "📍 地址: http://localhost:3000"
echo ""
echo "按 Ctrl+C 停止服务器"
echo "================================================"
echo ""

# Start the dev server
npm run dev

