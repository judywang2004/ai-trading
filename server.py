from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import openai
import os
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="AI Trading Analyzer API")

# Get allowed origins from environment (comma-separated list)
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
allowed_origins = [origin.strip() for origin in allowed_origins_str.split(",")]

# Configure CORS with secure settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Specific origins only
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("WARNING: OPENAI_API_KEY not found in environment variables!")

# Trading analysis prompt - Enhanced version
TRADING_ANALYSIS_PROMPT = """You are a professional trading analyst with 15+ years of experience in technical analysis. Analyze this trading chart thoroughly and provide an in-depth, actionable trading analysis.

## Analysis Framework:

### 1. Chart Overview
- Asset/Symbol identification (if visible)
- Timeframe analysis
- Current price level and recent price action

### 2. Technical Pattern Recognition
- Identify ALL chart patterns (head & shoulders, double top/bottom, triangles, wedges, flags, pennants, channels, etc.)
- Pattern confirmation status and reliability
- Historical pattern performance context
- Pattern targets and invalidation levels

### 3. Trend Analysis
- Primary trend direction (uptrend/downtrend/sideways)
- Trend strength (strong/moderate/weak)
- Higher highs/higher lows or lower highs/lower lows
- Potential trend reversal signals
- Multiple timeframe trend alignment

### 4. Support & Resistance Analysis
- Major support levels (list at least 3 with price levels)
- Major resistance levels (list at least 3 with price levels)
- Dynamic support/resistance (moving averages)
- Historical significance of these levels
- Confluence zones (where multiple levels align)

### 5. Technical Indicators Deep Dive
Analyze ALL visible indicators:
- **Moving Averages**: Crossovers, slopes, dynamic support/resistance
- **RSI**: Overbought/oversold conditions, divergences, trend
- **MACD**: Signal crossovers, histogram, divergences
- **Volume**: Volume spikes, volume trends, volume confirmation
- **Bollinger Bands**: Squeeze, expansion, price position
- **Stochastic**: Overbought/oversold, divergences
- Any other visible indicators

### 6. Market Structure
- Key swing highs and swing lows
- Market phases (accumulation, markup, distribution, markdown)
- Liquidity zones
- Order flow implications

### 7. Price Action Analysis
- Candlestick patterns (engulfing, doji, hammer, shooting star, etc.)
- Price rejection points
- Breakout or breakdown scenarios
- Gap analysis if any

### 8. Trading Strategy & Execution Plan

**LONG Setup (if applicable):**
- Entry zone: [specific price range]
- Stop loss: [specific price with reasoning]
- Target 1: [conservative target with price]
- Target 2: [moderate target with price]
- Target 3: [aggressive target with price]
- Risk/Reward ratio: [calculate specific ratio]
- Position sizing recommendation
- Entry confirmation signals to wait for

**SHORT Setup (if applicable):**
- Entry zone: [specific price range]
- Stop loss: [specific price with reasoning]
- Target 1: [conservative target with price]
- Target 2: [moderate target with price]
- Target 3: [aggressive target with price]
- Risk/Reward ratio: [calculate specific ratio]
- Position sizing recommendation
- Entry confirmation signals to wait for

### 9. Scenario Analysis
- **Bullish Scenario**: What needs to happen, probability, price targets
- **Bearish Scenario**: What needs to happen, probability, price targets
- **Neutral Scenario**: Sideways action, range bounds

### 10. Risk Assessment
- Major risk factors
- Potential fake-out scenarios
- External factors to monitor (news, events)
- Volatility considerations

### 11. Trade Management
- When to take partial profits
- How to trail stop loss
- Signs to exit early
- Position adjustment strategies

### 12. Market Sentiment & Confidence
- Overall market sentiment (bullish/bearish/neutral)
- Confidence level in analysis (High/Medium/Low)
- Key levels to watch for sentiment shift

### 13. Timeline & Monitoring
- Expected timeframe for setup to play out
- Key levels to monitor
- Important upcoming events or data releases

## Formatting Requirements:
- Use clear headings and bullet points
- Provide SPECIFIC price levels (not vague descriptions)
- Include percentage moves where relevant
- Be decisive but acknowledge uncertainty where it exists
- Prioritize the most important information first

Provide a comprehensive, professional analysis that institutional traders would find valuable."""


def validate_image(file: UploadFile) -> bool:
    """Validate that the uploaded file is an image"""
    if not file.content_type or not file.content_type.startswith("image/"):
        return False
    return True


def encode_image_to_base64(image_bytes: bytes) -> str:
    """Convert image bytes to base64 string"""
    return base64.b64encode(image_bytes).decode('utf-8')


async def analyze_trading_chart(image_bytes: bytes, filename: str) -> str:
    """
    Use OpenAI Vision API to analyze trading chart
    """
    try:
        print(f"\n{'='*60}")
        print(f"🔍 [DEBUG] 开始分析图片")
        print(f"📁 [DEBUG] 文件名: {filename}")
        print(f"📊 [DEBUG] 图片大小: {len(image_bytes)} bytes")
        
        # Encode image to base64 (reuse the same buffer)
        base64_image = encode_image_to_base64(image_bytes)
        print(f"✅ [DEBUG] Base64 编码完成，长度: {len(base64_image)}")
        
        # Determine image format from filename
        image_format = filename.split('.')[-1].lower()
        if image_format == 'jpg':
            image_format = 'jpeg'
        print(f"📷 [DEBUG] 图片格式: {image_format}")
        
        # Create the API call to OpenAI with vision
        client = openai.OpenAI(api_key=openai.api_key)
        print(f"🔑 [DEBUG] OpenAI 客户端已创建")
        print(f"🚀 [DEBUG] 正在调用 GPT-4 Vision API...")
        
        response = client.chat.completions.create(
            model="gpt-4o",  # GPT-4 with vision capabilities
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": TRADING_ANALYSIS_PROMPT
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{image_format};base64,{base64_image}",
                                "detail": "high"
                            }
                        }
                    ]
                }
            ],
            max_tokens=4000,  # Increased for more detailed analysis
            temperature=0.3  # Lower for more focused, precise analysis
        )
        
        print(f"✅ [DEBUG] OpenAI API 调用成功!")
        print(f"📝 [DEBUG] 响应模型: {response.model}")
        print(f"💰 [DEBUG] Token 使用: {response.usage.total_tokens if response.usage else 'N/A'}")
        
        analysis = response.choices[0].message.content
        print(f"📄 [DEBUG] 分析结果长度: {len(analysis)} 字符")
        print(f"🔤 [DEBUG] 分析结果前100字符: {analysis[:100]}...")
        print(f"{'='*60}\n")
        
        return analysis
        
    except openai.OpenAIError as e:
        print(f"❌ [ERROR] OpenAI API 错误: {str(e)}")
        print(f"❌ [ERROR] 错误类型: {type(e).__name__}")
        raise HTTPException(
            status_code=500,
            detail=f"OpenAI API error: {str(e)}"
        )
    except Exception as e:
        print(f"❌ [ERROR] 分析图片时出错: {str(e)}")
        print(f"❌ [ERROR] 错误类型: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing image: {str(e)}"
        )


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "AI Trading Analyzer API",
        "version": "1.0.0"
    }


@app.post("/api/upload")
async def upload_chart(file: UploadFile = File(...)):
    """
    Upload and analyze a trading chart image
    
    Args:
        file: The uploaded image file
        
    Returns:
        JSON with analysis and timestamp
    """
    print(f"\n🎯 [REQUEST] 收到上传请求")
    print(f"📁 [REQUEST] 文件名: {file.filename}")
    print(f"🏷️  [REQUEST] 内容类型: {file.content_type}")
    
    # Validate file type
    if not validate_image(file):
        print(f"❌ [ERROR] 文件类型验证失败")
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an image file."
        )
    
    # Check file size limit (10MB)
    max_size = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10")) * 1024 * 1024
    
    try:
        # Read image bytes ONCE
        image_bytes = await file.read()
        
        # Check file size
        if len(image_bytes) > max_size:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size is {max_size // (1024 * 1024)}MB"
            )
        
        # Validate image can be opened (reuse the same buffer)
        try:
            img = Image.open(BytesIO(image_bytes))
            img.verify()
            
            # Reopen to get actual image (verify closes it)
            img = Image.open(BytesIO(image_bytes))
            
            # Optional: Downscale large images to reduce processing cost
            max_dimension = int(os.getenv("MAX_IMAGE_DIMENSION", "2048"))
            if max(img.size) > max_dimension:
                img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
                # Convert back to bytes
                buffer = BytesIO()
                img_format = img.format or 'PNG'
                img.save(buffer, format=img_format)
                image_bytes = buffer.getvalue()
                
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid or corrupted image file: {str(e)}"
            )
        
        # Analyze the trading chart using OpenAI (reuse image_bytes)
        print(f"📤 [INFO] 发送到 OpenAI 进行分析...")
        analysis = await analyze_trading_chart(image_bytes, file.filename or "chart.png")
        
        print(f"✅ [SUCCESS] 分析完成，准备返回结果")
        
        # Return the analysis with timestamp
        result = {
            "analysis": analysis,
            "timestamp": datetime.now().isoformat(),
            "filename": file.filename
        }
        print(f"📦 [RESPONSE] 返回结果，分析长度: {len(analysis)} 字符")
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )
    finally:
        await file.close()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )


