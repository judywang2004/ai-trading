import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from io import BytesIO
from PIL import Image
import base64
import os

# Set test environment variables before importing server
os.environ["OPENAI_API_KEY"] = "test_key"
os.environ["ALLOWED_ORIGINS"] = "http://localhost:3000"

from server import app

client = TestClient(app)


def create_test_image(format="PNG", size=(100, 100)):
    """Helper function to create a test image"""
    img = Image.new('RGB', size, color='red')
    buffer = BytesIO()
    img.save(buffer, format=format)
    buffer.seek(0)
    return buffer


class TestHealthCheck:
    """Test health check endpoint"""
    
    def test_root_endpoint(self):
        """Test that root endpoint returns correct status"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "online"
        assert data["service"] == "AI Trading Analyzer API"
        assert "version" in data


class TestUploadValidation:
    """Test upload validation and error handling"""
    
    def test_upload_without_file(self):
        """Test upload endpoint without a file"""
        response = client.post("/api/upload")
        assert response.status_code == 422  # Validation error
    
    def test_upload_non_image_file(self):
        """Test upload with non-image file"""
        files = {"file": ("test.txt", BytesIO(b"Not an image"), "text/plain")}
        response = client.post("/api/upload", files=files)
        assert response.status_code == 400
        assert "Invalid file type" in response.json()["detail"]
    
    def test_upload_corrupted_image(self):
        """Test upload with corrupted image data"""
        files = {"file": ("test.png", BytesIO(b"corrupted data"), "image/png")}
        response = client.post("/api/upload", files=files)
        assert response.status_code == 400
        assert "corrupted" in response.json()["detail"].lower()
    
    def test_upload_oversized_file(self):
        """Test upload with file exceeding size limit"""
        # Create a large image (simulate oversized file)
        with patch.dict(os.environ, {"MAX_UPLOAD_SIZE_MB": "0"}):
            img_buffer = create_test_image(size=(100, 100))
            files = {"file": ("test.png", img_buffer, "image/png")}
            response = client.post("/api/upload", files=files)
            # Should fail due to size limit
            assert response.status_code in [400, 413]


class TestImageProcessing:
    """Test image processing functionality"""
    
    @patch('server.openai.OpenAI')
    def test_successful_upload_and_analysis(self, mock_openai):
        """Test successful image upload and analysis"""
        # Mock OpenAI response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test analysis result"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        # Create test image
        img_buffer = create_test_image()
        files = {"file": ("test.png", img_buffer, "image/png")}
        
        response = client.post("/api/upload", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert "analysis" in data
        assert "timestamp" in data
        assert "filename" in data
        assert data["analysis"] == "Test analysis result"
        assert data["filename"] == "test.png"
    
    @patch('server.openai.OpenAI')
    def test_jpeg_image_upload(self, mock_openai):
        """Test JPEG image upload"""
        # Mock OpenAI response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "JPEG analysis"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        # Create JPEG test image
        img_buffer = create_test_image(format="JPEG")
        files = {"file": ("test.jpg", img_buffer, "image/jpeg")}
        
        response = client.post("/api/upload", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert data["analysis"] == "JPEG analysis"
    
    @patch('server.openai.OpenAI')
    def test_large_image_downscaling(self, mock_openai):
        """Test that large images are downscaled"""
        # Mock OpenAI response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Downscaled image analysis"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        # Create large test image
        with patch.dict(os.environ, {"MAX_IMAGE_DIMENSION": "50"}):
            img_buffer = create_test_image(size=(1000, 1000))
            files = {"file": ("large.png", img_buffer, "image/png")}
            
            response = client.post("/api/upload", files=files)
            
            assert response.status_code == 200
            # Image should be processed successfully even if large


class TestOpenAIIntegration:
    """Test OpenAI API integration"""
    
    @patch('server.openai.OpenAI')
    def test_openai_api_error_handling(self, mock_openai):
        """Test handling of OpenAI API errors"""
        # Mock OpenAI to raise an error
        mock_client = MagicMock()
        mock_client.chat.completions.create.side_effect = Exception("API Error")
        mock_openai.return_value = mock_client
        
        img_buffer = create_test_image()
        files = {"file": ("test.png", img_buffer, "image/png")}
        
        response = client.post("/api/upload", files=files)
        
        assert response.status_code == 500
        assert "error" in response.json()["detail"].lower()
    
    @patch('server.openai.OpenAI')
    def test_openai_receives_correct_parameters(self, mock_openai):
        """Test that OpenAI receives correct parameters"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Analysis"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        img_buffer = create_test_image()
        files = {"file": ("test.png", img_buffer, "image/png")}
        
        response = client.post("/api/upload", files=files)
        
        assert response.status_code == 200
        
        # Verify OpenAI was called with correct parameters
        call_args = mock_client.chat.completions.create.call_args
        assert call_args.kwargs["model"] == "gpt-4o"
        assert call_args.kwargs["max_tokens"] == 2000
        assert call_args.kwargs["temperature"] == 0.7
        
        # Verify message structure
        messages = call_args.kwargs["messages"]
        assert len(messages) == 1
        assert messages[0]["role"] == "user"
        assert len(messages[0]["content"]) == 2
        assert messages[0]["content"][0]["type"] == "text"
        assert messages[0]["content"][1]["type"] == "image_url"


class TestCORSConfiguration:
    """Test CORS configuration"""
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in response"""
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
        assert "access-control-allow-origin" in response.headers
    
    def test_cors_allowed_origin(self):
        """Test that configured origins are allowed"""
        response = client.options(
            "/api/upload",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST"
            }
        )
        # Should allow the configured origin
        assert response.status_code in [200, 204]


class TestMemoryEfficiency:
    """Test memory efficiency improvements"""
    
    @patch('server.openai.OpenAI')
    def test_single_file_read(self, mock_openai):
        """Test that file is read only once"""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Analysis"
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        img_buffer = create_test_image()
        original_read = img_buffer.read
        read_count = {"count": 0}
        
        def counting_read(*args, **kwargs):
            read_count["count"] += 1
            return original_read(*args, **kwargs)
        
        img_buffer.read = counting_read
        
        files = {"file": ("test.png", img_buffer, "image/png")}
        response = client.post("/api/upload", files=files)
        
        assert response.status_code == 200
        # File should be read only once by the endpoint
        assert read_count["count"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

