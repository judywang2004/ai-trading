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

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    print("WARNING: OPENAI_API_KEY not found in environment variables!")

# Trading analysis prompt
TRADING_ANALYSIS_PROMPT = """You are an expert trading analyst. Analyze this trading chart image and provide a comprehensive trading analysis including:

1. **Chart Pattern Recognition**: Identify any technical patterns (head and shoulders, triangles, flags, etc.)
2. **Trend Analysis**: Determine the current trend (uptrend, downtrend, sideways)
3. **Support & Resistance Levels**: Identify key support and resistance levels
4. **Technical Indicators**: Analyze any visible indicators (RSI, MACD, Moving Averages, etc.)
5. **Volume Analysis**: Comment on volume patterns if visible
6. **Trading Strategy**: Provide specific trading recommendations:
   - Entry points
   - Stop loss levels
   - Take profit targets
   - Risk/reward ratio
7. **Market Sentiment**: Overall market sentiment and confidence level
8. **Risk Assessment**: Potential risks and warnings

Please provide a detailed, actionable analysis that a trader can use to make informed decisions."""


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
        # Encode image to base64
        base64_image = encode_image_to_base64(image_bytes)
        
        # Determine image format from filename
        image_format = filename.split('.')[-1].lower()
        if image_format == 'jpg':
            image_format = 'jpeg'
        
        # Create the API call to OpenAI with vision
        client = openai.OpenAI(api_key=openai.api_key)
        
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
            max_tokens=2000,
            temperature=0.7
        )
        
        analysis = response.choices[0].message.content
        return analysis
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error analyzing image with OpenAI: {str(e)}"
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
    # Validate file type
    if not validate_image(file):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an image file."
        )
    
    try:
        # Read image bytes
        image_bytes = await file.read()
        
        # Validate image can be opened
        try:
            img = Image.open(BytesIO(image_bytes))
            img.verify()
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail="Invalid or corrupted image file"
            )
        
        # Reset file pointer after verify
        image_bytes = await file.read()
        await file.seek(0)
        image_bytes = await file.read()
        
        # Analyze the trading chart using OpenAI
        analysis = await analyze_trading_chart(image_bytes, file.filename or "chart.png")
        
        # Return the analysis with timestamp
        return JSONResponse(
            content={
                "analysis": analysis,
                "timestamp": datetime.now().isoformat(),
                "filename": file.filename
            }
        )
        
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


