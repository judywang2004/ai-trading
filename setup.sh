#!/bin/bash

# AI Trading Analyzer - Complete Setup Script
# 完整安装脚本

echo "================================================"
echo "🚀 AI Trading Analyzer - 自动安装脚本"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo "📦 检查 Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 未找到 Python 3${NC}"
    echo "请先安装 Python 3.8 或更高版本"
    exit 1
fi
echo -e "${GREEN}✅ Python: $(python3 --version)${NC}"

# Check Node.js
echo "📦 检查 Node.js..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}❌ 未找到 Node.js${NC}"
    echo "请先安装 Node.js 16 或更高版本"
    exit 1
fi
echo -e "${GREEN}✅ Node.js: $(node --version)${NC}"
echo -e "${GREEN}✅ npm: $(npm --version)${NC}"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  未找到 .env 文件${NC}"
    echo "正在创建 .env 文件..."
    echo ""
    
    # Prompt for OpenAI API key
    read -p "请输入你的 OpenAI API 密钥: " openai_key
    
    if [ -z "$openai_key" ]; then
        echo -e "${RED}❌ 必须提供 OpenAI API 密钥${NC}"
        exit 1
    fi
    
    # Create .env file
    cat > .env << EOF
# OpenAI API Configuration
OPENAI_API_KEY=$openai_key

# Server Configuration
PORT=8000

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:3000

# Upload Configuration
MAX_UPLOAD_SIZE_MB=10
MAX_IMAGE_DIMENSION=2048
EOF
    
    echo -e "${GREEN}✅ 已创建 .env 文件${NC}"
    echo ""
else
    echo -e "${GREEN}✅ 找到 .env 文件${NC}"
fi

# Install Python dependencies
echo "📦 安装 Python 依赖..."
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Python 依赖安装成功${NC}"
else
    echo -e "${RED}❌ Python 依赖安装失败${NC}"
    exit 1
fi
echo ""

# Install Node dependencies
echo "📦 安装 Node.js 依赖..."
npm install
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Node.js 依赖安装成功${NC}"
else
    echo -e "${RED}❌ Node.js 依赖安装失败${NC}"
    exit 1
fi
echo ""

# Run tests
echo "🧪 运行测试..."
pytest test_server.py -q
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ 所有测试通过${NC}"
else
    echo -e "${YELLOW}⚠️  有些测试失败，但可以继续${NC}"
fi
echo ""

echo "================================================"
echo -e "${GREEN}🎉 安装完成！${NC}"
echo "================================================"
echo ""
echo "📝 下一步："
echo ""
echo "1️⃣  启动后端服务器（新终端窗口）："
echo "   ./start_backend.sh"
echo ""
echo "2️⃣  启动前端服务器（新终端窗口）："
echo "   ./start_frontend.sh"
echo ""
echo "3️⃣  在浏览器中打开："
echo "   http://localhost:3000"
echo ""
echo "================================================"

