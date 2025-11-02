# AI Trading Analyzer

An AI-powered trading chart analysis application that uses OpenAI's GPT-4 Vision API to provide comprehensive trading insights and strategies.

## Features

- 🖼️ **Image Upload**: Drag-and-drop or browse to upload trading charts
- 🤖 **AI Analysis**: Powered by GPT-4 Vision for intelligent chart analysis
- 📊 **Comprehensive Insights**: Get detailed analysis including:
  - Chart pattern recognition
  - Trend analysis
  - Support & resistance levels
  - Technical indicators interpretation
  - Volume analysis
  - Trading strategy recommendations (entry/exit points, stop loss, take profit)
  - Risk assessment

## Tech Stack

### Frontend
- **React** with TypeScript
- **Vite** for fast development
- **Axios** for API calls
- **Lucide React** for icons

### Backend
- **FastAPI** for high-performance API
- **OpenAI GPT-4 Vision** for image analysis
- **Python 3.8+**

## Prerequisites

- Node.js 16+ and npm/yarn
- Python 3.8+
- OpenAI API key with GPT-4 Vision access

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ai_trading
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```
OPENAI_API_KEY=your_actual_openai_api_key_here
PORT=8000
```

### 3. Backend Setup

Install Python dependencies:

```bash
pip install -r requirements.txt
```

### 4. Frontend Setup

Install Node dependencies:

```bash
npm install
```

## Running the Application

### Start Backend Server

```bash
python server.py
```

The backend will run on `http://localhost:8000`

### Start Frontend Development Server

In a separate terminal:

```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Upload a trading chart image by:
   - Dragging and dropping the image onto the upload area, or
   - Clicking "Browse Files" to select an image
3. Click "Analyze Chart" button
4. Wait for the AI analysis (usually takes 5-15 seconds)
5. Review the comprehensive trading analysis and recommendations

## API Endpoints

### `GET /`
Health check endpoint

**Response:**
```json
{
  "status": "online",
  "service": "AI Trading Analyzer API",
  "version": "1.0.0"
}
```

### `POST /api/upload`
Upload and analyze a trading chart

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (image file)

**Response:**
```json
{
  "analysis": "Detailed trading analysis text...",
  "timestamp": "2025-11-02T10:30:00.000000",
  "filename": "chart.png"
}
```

## Building for Production

### Frontend Build

```bash
npm run build
```

The production-ready files will be in the `dist/` directory.

### Backend Production

Use a production ASGI server like Gunicorn:

```bash
gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Security Notes

- Never commit your `.env` file or expose your OpenAI API key
- In production, update CORS settings in `server.py` to allow only specific origins
- Consider implementing rate limiting to prevent API abuse
- Add authentication if deploying publicly

## Troubleshooting

### "OPENAI_API_KEY not found"
Make sure you've created a `.env` file with your OpenAI API key.

### CORS Errors
Ensure both frontend and backend servers are running and the proxy is configured correctly in `vite.config.ts`.

### Image Upload Fails
Check that the file is a valid image format (JPEG, PNG, GIF, WebP) and not corrupted.

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

