import pytest
import json
from unittest.mock import patch, MagicMock
from ai.groq_service import GroqService
from config import Config


@pytest.fixture(autouse=True)
def setup_config():
    # Store old values
    old_key = Config.GROQ_API_KEY
    old_model = Config.GROQ_MODEL
    old_fallback = Config.GROQ_FALLBACK_MODEL
    
    # Set test values
    Config.GROQ_API_KEY = "test_key"
    Config.GROQ_MODEL = "openai/gpt-oss-120b"
    Config.GROQ_FALLBACK_MODEL = "qwen/qwen3-32b"
    
    yield
    
    # Restore
    Config.GROQ_API_KEY = old_key
    Config.GROQ_MODEL = old_model
    Config.GROQ_FALLBACK_MODEL = old_fallback


@patch("urllib.request.urlopen")
def test_groq_service_success(mock_urlopen):
    # Mock successful response
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({
        "choices": [{
            "message": {
                "content": "Success content"
            }
        }]
    }).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_resp

    service = GroqService()
    result = service.generate("Hello")
    assert result == "Success content"
    
    # Verify it called once
    assert mock_urlopen.call_count == 1


@patch("urllib.request.urlopen")
def test_groq_service_fallback(mock_urlopen):
    # First call fails, second call succeeds
    mock_resp_fail = MagicMock()
    mock_resp_fail.side_effect = Exception("Primary model error")
    
    mock_resp_success = MagicMock()
    mock_resp_success.read.return_value = json.dumps({
        "choices": [{
            "message": {
                "content": "Fallback content"
            }
        }]
    }).encode("utf-8")
    
    # urlopen enters a context manager. 
    # Side effects for calls to __enter__:
    mock_context = MagicMock()
    mock_context.__enter__.side_effect = [Exception("Primary model error"), mock_resp_success]
    mock_urlopen.return_value = mock_context

    service = GroqService()
    result = service.generate("Hello")
    assert result == "Fallback content"
    assert mock_urlopen.call_count == 2


@patch("urllib.request.urlopen")
def test_groq_service_double_failure(mock_urlopen):
    # Both calls fail
    mock_context = MagicMock()
    mock_context.__enter__.side_effect = [Exception("Primary error"), Exception("Fallback error")]
    mock_urlopen.return_value = mock_context

    service = GroqService()
    result = service.generate("Hello")
    assert "Primary model" in result
    assert "Fallback model" in result
    assert mock_urlopen.call_count == 2


@patch("urllib.request.urlopen")
def test_groq_service_model_override(mock_urlopen):
    mock_resp = MagicMock()
    mock_resp.read.return_value = json.dumps({
        "choices": [{
            "message": {
                "content": "Mapped content"
            }
        }]
    }).encode("utf-8")
    mock_urlopen.return_value.__enter__.return_value = mock_resp

    old_url = Config.GROQ_API_URL
    Config.GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
    try:
        service = GroqService()
        result = service.generate("Hello")
        assert result == "Mapped content"
        
        args, kwargs = mock_urlopen.call_args
        req = args[0]
        data = json.loads(req.data.decode("utf-8"))
        assert data["model"] == "llama-3.3-70b-versatile"
    finally:
        Config.GROQ_API_URL = old_url
