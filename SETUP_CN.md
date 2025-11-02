# AI 交易分析器 - 详细运行步骤

## 📋 前置要求

确保你的电脑已安装：
- ✅ Python 3.8 或更高版本
- ✅ Node.js 16 或更高版本
- ✅ npm（随 Node.js 一起安装）
- ✅ OpenAI API 密钥（需要 GPT-4 Vision 访问权限）

## 🚀 完整运行步骤

### 步骤 1: 检查环境

打开终端，运行以下命令检查版本：

```bash
# 检查 Python 版本（应该是 3.8+）
python3 --version

# 检查 Node.js 版本（应该是 16+）
node --version

# 检查 npm 版本
npm --version
```

### 步骤 2: 进入项目目录

```bash
cd /Users/judywang/Documents/ai_trading
```

### 步骤 3: 配置环境变量

创建 `.env` 文件：

```bash
touch .env
```

用文本编辑器打开 `.env` 文件，添加以下内容：

```env
# 必需：你的 OpenAI API 密钥
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# 服务器配置
PORT=8000

# CORS 配置（允许的前端地址）
ALLOWED_ORIGINS=http://localhost:3000

# 上传限制
MAX_UPLOAD_SIZE_MB=10
MAX_IMAGE_DIMENSION=2048
```

**重要：** 将 `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` 替换为你真实的 OpenAI API 密钥

### 步骤 4: 安装后端依赖

```bash
pip3 install -r requirements.txt
```

如果遇到权限问题，可以使用：

```bash
pip3 install --user -r requirements.txt
```

### 步骤 5: 安装前端依赖

```bash
npm install
```

### 步骤 6: 运行测试（可选但推荐）

验证后端是否正确配置：

```bash
pytest test_server.py -v
```

如果所有测试通过，说明配置正确！✅

### 步骤 7: 启动后端服务器

打开一个新的终端窗口，运行：

```bash
cd /Users/judywang/Documents/ai_trading
python3 server.py
```

你应该看到类似这样的输出：

```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

**保持这个终端窗口运行！**

### 步骤 8: 启动前端开发服务器

打开**另一个新的**终端窗口，运行：

```bash
cd /Users/judywang/Documents/ai_trading
npm run dev
```

你应该看到类似这样的输出：

```
  VITE v5.0.8  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

### 步骤 9: 打开应用

在浏览器中访问：**http://localhost:3000**

## 🎯 使用应用

1. **上传图片**：
   - 拖拽交易图表到上传区域
   - 或点击 "Browse Files" 按钮选择文件

2. **分析图表**：
   - 点击 "Analyze Chart" 按钮
   - 等待 5-15 秒（AI 正在分析）

3. **查看结果**：
   - 查看详细的交易分析报告
   - 包括趋势、支撑/阻力位、入场/出场点等

4. **新分析**：
   - 点击 "New Analysis" 开始新的分析

## 🔧 常见问题解决

### 问题 1: "OPENAI_API_KEY not found"

**解决方案：**
- 确保已创建 `.env` 文件
- 确保 API 密钥正确无误
- 重启后端服务器

### 问题 2: 端口被占用

如果 8000 或 3000 端口被占用：

**方法 1 - 更改端口：**
```bash
# 在 .env 文件中
PORT=8001

# 在另一个终端运行前端时
PORT=3001 npm run dev
```

**方法 2 - 停止占用端口的进程：**
```bash
# 查找占用 8000 端口的进程
lsof -ti:8000

# 停止该进程（替换 PID 为上面命令返回的进程 ID）
kill -9 PID
```

### 问题 3: CORS 错误

**解决方案：**
- 确保两个服务器都在运行
- 检查 `.env` 文件中的 `ALLOWED_ORIGINS` 包含 `http://localhost:3000`
- 重启后端服务器

### 问题 4: 图片上传失败

**解决方案：**
- 确保文件是图片格式（JPEG, PNG, GIF, WebP）
- 确保文件小于 10MB
- 确保图片没有损坏

### 问题 5: 测试失败

**解决方案：**
```bash
# 确保安装了测试依赖
pip3 install pytest pytest-asyncio "httpx<0.28"

# 重新运行测试
pytest test_server.py -v
```

## 📝 快速启动脚本

你也可以创建启动脚本方便以后使用。

### 创建后端启动脚本 `start_backend.sh`：

```bash
#!/bin/bash
cd /Users/judywang/Documents/ai_trading
echo "🚀 启动后端服务器..."
python3 server.py
```

### 创建前端启动脚本 `start_frontend.sh`：

```bash
#!/bin/bash
cd /Users/judywang/Documents/ai_trading
echo "🚀 启动前端服务器..."
npm run dev
```

### 赋予执行权限：

```bash
chmod +x start_backend.sh start_frontend.sh
```

### 使用脚本启动：

```bash
# 终端 1
./start_backend.sh

# 终端 2
./start_frontend.sh
```

## 🎉 成功标志

如果一切正常，你应该：
- ✅ 能在浏览器访问 http://localhost:3000
- ✅ 看到一个漂亮的 UI 界面
- ✅ 能够上传图片
- ✅ 能够获得 AI 分析结果

## 📞 需要帮助？

如果遇到其他问题，请检查：
1. 两个终端窗口是否都在运行
2. `.env` 文件配置是否正确
3. 所有依赖是否都已安装
4. OpenAI API 密钥是否有效且有 GPT-4 Vision 权限

祝你使用愉快！🚀

