import { useState } from 'react'
import axios from 'axios'
import { Upload, TrendingUp, AlertCircle, Loader2, ImageIcon } from 'lucide-react'
import './App.css'

interface AnalysisResult {
  analysis: string
  timestamp: string
}

function App() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState<string | null>(null)

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      setSelectedFile(file)
      setPreviewUrl(URL.createObjectURL(file))
      setResult(null)
      setError(null)
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) return

    setLoading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const response = await axios.post<AnalysisResult>('/api/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      setResult(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to analyze image. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    
    const file = e.dataTransfer.files?.[0]
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file)
      setPreviewUrl(URL.createObjectURL(file))
      setResult(null)
      setError(null)
    }
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <div className="header-icon">
            <TrendingUp size={40} />
          </div>
          <h1>AI Trading Analyzer</h1>
          <p className="subtitle">Upload trading charts and get AI-powered analysis</p>
        </header>

        <div className="upload-section">
          <div
            className={`upload-area ${selectedFile ? 'has-file' : ''}`}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
          >
            {previewUrl ? (
              <div className="preview-container">
                <img src={previewUrl} alt="Preview" className="preview-image" />
                <button
                  className="change-image-btn"
                  onClick={() => document.getElementById('file-input')?.click()}
                >
                  Change Image
                </button>
              </div>
            ) : (
              <>
                <ImageIcon size={64} className="upload-icon" />
                <h3>Drop your trading chart here</h3>
                <p>or click to browse</p>
                <input
                  id="file-input"
                  type="file"
                  accept="image/*"
                  onChange={handleFileSelect}
                  style={{ display: 'none' }}
                />
                <button
                  className="browse-btn"
                  onClick={() => document.getElementById('file-input')?.click()}
                >
                  <Upload size={20} />
                  Browse Files
                </button>
              </>
            )}
          </div>

          {selectedFile && !result && (
            <button
              className="analyze-btn"
              onClick={handleUpload}
              disabled={loading}
            >
              {loading ? (
                <>
                  <Loader2 size={20} className="spinner" />
                  Analyzing...
                </>
              ) : (
                <>
                  <TrendingUp size={20} />
                  Analyze Chart
                </>
              )}
            </button>
          )}
        </div>

        {error && (
          <div className="error-box">
            <AlertCircle size={20} />
            <span>{error}</span>
          </div>
        )}

        {result && (
          <div className="result-section">
            <div className="result-header">
              <TrendingUp size={24} />
              <h2>Trading Analysis</h2>
            </div>
            <div className="result-content">
              <div className="analysis-text">
                {result.analysis.split('\n').map((line, index) => (
                  <p key={index}>{line}</p>
                ))}
              </div>
              <div className="result-footer">
                <span className="timestamp">
                  Analyzed at {new Date(result.timestamp).toLocaleString()}
                </span>
              </div>
            </div>
            <button
              className="new-analysis-btn"
              onClick={() => {
                setSelectedFile(null)
                setPreviewUrl(null)
                setResult(null)
                setError(null)
              }}
            >
              New Analysis
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default App



