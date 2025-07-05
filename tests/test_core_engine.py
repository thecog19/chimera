"""Unit tests for the Core Engine ComparativeTokenizer class."""

import pytest
from unittest.mock import Mock, patch
from src.core_engine import ComparativeTokenizer


class TestComparativeTokenizer:
    """Test suite for the ComparativeTokenizer class."""
    
    def test_init_creates_tokenizers(self) -> None:
        """Test that __init__ successfully creates tokenizer instances."""
        with patch('tiktoken.encoding_for_model') as mock_tiktoken, \
             patch('transformers.AutoTokenizer.from_pretrained') as mock_transformers:
            
            mock_tiktoken.return_value = Mock()
            mock_transformers.return_value = Mock()
            
            tokenizer = ComparativeTokenizer()
            
            assert "gpt-4o" in tokenizer.tokenizers
            assert "Llama-3-8B" in tokenizer.tokenizers
            mock_tiktoken.assert_called_once_with("gpt-4o")
            mock_transformers.assert_called_once_with("meta-llama/Meta-Llama-3-8B-Instruct")
    
    def test_analyze_returns_correct_structure(self) -> None:
        """Test that analyze returns the expected dictionary structure."""
        with patch('tiktoken.encoding_for_model') as mock_tiktoken, \
             patch('transformers.AutoTokenizer.from_pretrained') as mock_transformers:
            
            # Mock gpt-4o tokenizer
            mock_gpt4o = Mock()
            mock_gpt4o.encode.return_value = [1, 2, 3]
            mock_gpt4o.decode.side_effect = lambda x: f"token_{x[0]}"
            mock_tiktoken.return_value = mock_gpt4o
            
            # Mock Llama tokenizer
            mock_llama = Mock()
            mock_llama.encode.return_value = [4, 5, 6]
            mock_llama.convert_ids_to_tokens.return_value = ["token_4", "token_5", "token_6"]
            mock_transformers.return_value = mock_llama
            
            tokenizer = ComparativeTokenizer()
            result = tokenizer.analyze("test string")
            
            assert isinstance(result, dict)
            assert "gpt-4o" in result
            assert "Llama-3-8B" in result
            
            # Check gpt-4o structure
            assert "tokens" in result["gpt-4o"]
            assert "ids" in result["gpt-4o"]
            assert isinstance(result["gpt-4o"]["tokens"], list)
            assert isinstance(result["gpt-4o"]["ids"], list)
            
            # Check Llama structure
            assert "tokens" in result["Llama-3-8B"]
            assert "ids" in result["Llama-3-8B"]
            assert isinstance(result["Llama-3-8B"]["tokens"], list)
            assert isinstance(result["Llama-3-8B"]["ids"], list)
    
    def test_analyze_with_empty_string(self) -> None:
        """Test analyze method with empty string input."""
        with patch('tiktoken.encoding_for_model') as mock_tiktoken, \
             patch('transformers.AutoTokenizer.from_pretrained') as mock_transformers:
            
            mock_gpt4o = Mock()
            mock_gpt4o.encode.return_value = []
            mock_tiktoken.return_value = mock_gpt4o
            
            mock_llama = Mock()
            mock_llama.encode.return_value = []
            mock_llama.convert_ids_to_tokens.return_value = []
            mock_transformers.return_value = mock_llama
            
            tokenizer = ComparativeTokenizer()
            result = tokenizer.analyze("")
            
            assert result["gpt-4o"]["tokens"] == []
            assert result["gpt-4o"]["ids"] == []
            assert result["Llama-3-8B"]["tokens"] == []
            assert result["Llama-3-8B"]["ids"] == []
    
    def test_analyze_calls_tokenizer_methods(self) -> None:
        """Test that analyze calls the correct tokenizer methods."""
        with patch('tiktoken.encoding_for_model') as mock_tiktoken, \
             patch('transformers.AutoTokenizer.from_pretrained') as mock_transformers:
            
            mock_gpt4o = Mock()
            mock_gpt4o.encode.return_value = [1, 2]
            mock_gpt4o.decode.side_effect = lambda x: f"token_{x[0]}"
            mock_tiktoken.return_value = mock_gpt4o
            
            mock_llama = Mock()
            mock_llama.encode.return_value = [3, 4]
            mock_llama.convert_ids_to_tokens.return_value = ["token_3", "token_4"]
            mock_transformers.return_value = mock_llama
            
            tokenizer = ComparativeTokenizer()
            test_string = "test input"
            tokenizer.analyze(test_string)
            
            # Verify gpt-4o methods were called
            mock_gpt4o.encode.assert_called_once_with(test_string)
            assert mock_gpt4o.decode.call_count == 2  # Called for each token
            
            # Verify Llama methods were called
            mock_llama.encode.assert_called_once_with(test_string)
            mock_llama.convert_ids_to_tokens.assert_called_once_with([3, 4])
    
    def test_analyze_with_special_characters(self) -> None:
        """Test analyze method with special characters and unicode."""
        with patch('tiktoken.encoding_for_model') as mock_tiktoken, \
             patch('transformers.AutoTokenizer.from_pretrained') as mock_transformers:
            
            mock_gpt4o = Mock()
            mock_gpt4o.encode.return_value = [100, 101]
            mock_gpt4o.decode.side_effect = lambda x: f"special_{x[0]}"
            mock_tiktoken.return_value = mock_gpt4o
            
            mock_llama = Mock()
            mock_llama.encode.return_value = [200, 201]
            mock_llama.convert_ids_to_tokens.return_value = ["special_200", "special_201"]
            mock_transformers.return_value = mock_llama
            
            tokenizer = ComparativeTokenizer()
            special_string = "Hello! 🌟 测试"
            result = tokenizer.analyze(special_string)
            
            assert len(result["gpt-4o"]["tokens"]) == 2
            assert len(result["gpt-4o"]["ids"]) == 2
            assert len(result["Llama-3-8B"]["tokens"]) == 2
            assert len(result["Llama-3-8B"]["ids"]) == 2