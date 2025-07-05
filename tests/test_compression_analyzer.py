"""Unit tests for the CompressionAnomalyFinder class."""

import pytest
from unittest.mock import Mock
from discovery_modules.compression_analyzer import CompressionAnomalyFinder


class TestCompressionAnomalyFinder:
    """Test suite for the CompressionAnomalyFinder class."""
    
    def test_init_stores_tokenizer(self) -> None:
        """Test that __init__ stores the tokenizer instance."""
        mock_tokenizer = Mock()
        finder = CompressionAnomalyFinder(mock_tokenizer)
        
        assert finder.tokenizer == mock_tokenizer
    
    def test_find_anomalies_detects_high_compression(self) -> None:
        """Test that find_anomalies detects words with high compression ratios."""
        # Create mock tokenizer
        mock_tokenizer = Mock()
        mock_tokenizer.analyze.return_value = {
            "gpt-4o": {"tokens": ["test"], "ids": [1]},
            "Llama-3-8B": {"tokens": ["test"], "ids": [2]}
        }
        
        finder = CompressionAnomalyFinder(mock_tokenizer)
        
        # Test with a word that should trigger anomaly (20 chars, 1 token = ratio 20.0)
        word_list = ["verylongwordthatcomp"]  # 20 characters
        anomalies = finder.find_anomalies(word_list, threshold=10.0)
        
        # Should detect 2 anomalies (one for each tokenizer)
        assert len(anomalies) == 2
        
        # Check first anomaly
        anomaly = anomalies[0]
        assert anomaly["input_string"] == "verylongwordthatcomp"
        assert anomaly["target_tokenizer"] in ["gpt-4o", "Llama-3-8B"]
        assert anomaly["char_count"] == 20
        assert anomaly["token_count"] == 1
        assert anomaly["ratio"] == 20.0
    
    def test_find_anomalies_ignores_normal_words(self) -> None:
        """Test that find_anomalies ignores words with normal compression ratios."""
        # Create mock tokenizer that returns multiple tokens
        mock_tokenizer = Mock()
        mock_tokenizer.analyze.return_value = {
            "gpt-4o": {"tokens": ["test", "ing"], "ids": [1, 2]},
            "Llama-3-8B": {"tokens": ["test", "ing"], "ids": [3, 4]}
        }
        
        finder = CompressionAnomalyFinder(mock_tokenizer)
        
        # Test with a word that should NOT trigger anomaly (7 chars, 2 tokens = ratio 3.5)
        word_list = ["testing"]  # 7 characters
        anomalies = finder.find_anomalies(word_list, threshold=10.0)
        
        # Should detect no anomalies
        assert len(anomalies) == 0
    
    def test_find_anomalies_handles_empty_strings(self) -> None:
        """Test that find_anomalies handles empty strings gracefully."""
        mock_tokenizer = Mock()
        mock_tokenizer.analyze.return_value = {
            "gpt-4o": {"tokens": ["test"], "ids": [1]}
        }
        finder = CompressionAnomalyFinder(mock_tokenizer)
        
        word_list = ["", "  ", "test"]
        anomalies = finder.find_anomalies(word_list, threshold=10.0)
        
        # Should only process non-empty strings
        assert mock_tokenizer.analyze.call_count == 2  # Called for "  " and "test"
    
    def test_find_anomalies_handles_zero_tokens(self) -> None:
        """Test that find_anomalies handles zero token count without division error."""
        mock_tokenizer = Mock()
        mock_tokenizer.analyze.return_value = {
            "gpt-4o": {"tokens": [], "ids": []},
            "Llama-3-8B": {"tokens": [], "ids": []}
        }
        
        finder = CompressionAnomalyFinder(mock_tokenizer)
        
        word_list = ["test"]
        anomalies = finder.find_anomalies(word_list, threshold=10.0)
        
        # Should handle zero token count gracefully (ratio = 0.0)
        assert len(anomalies) == 0
    
    def test_find_anomalies_respects_threshold(self) -> None:
        """Test that find_anomalies respects the threshold parameter."""
        mock_tokenizer = Mock()
        mock_tokenizer.analyze.return_value = {
            "gpt-4o": {"tokens": ["test"], "ids": [1]}
        }
        
        finder = CompressionAnomalyFinder(mock_tokenizer)
        
        # Test with 10-character word (ratio = 10.0)
        word_list = ["tencharwrd"]  # 10 characters
        
        # With threshold 10.0, should not detect anomaly
        anomalies = finder.find_anomalies(word_list, threshold=10.0)
        assert len(anomalies) == 0
        
        # With threshold 9.0, should detect anomaly
        anomalies = finder.find_anomalies(word_list, threshold=9.0)
        assert len(anomalies) == 1
    
    def test_find_anomalies_multiple_words(self) -> None:
        """Test that find_anomalies processes multiple words correctly."""
        mock_tokenizer = Mock()
        
        def mock_analyze(word):
            if word == "short":
                return {"gpt-4o": {"tokens": ["sho", "rt"], "ids": [1, 2]}}
            elif word == "verylongwordthatcompresses":
                return {"gpt-4o": {"tokens": ["long"], "ids": [3]}}
            return {"gpt-4o": {"tokens": ["test"], "ids": [4]}}
        
        mock_tokenizer.analyze.side_effect = mock_analyze
        
        finder = CompressionAnomalyFinder(mock_tokenizer)
        
        word_list = ["short", "verylongwordthatcompresses", "normal"]
        anomalies = finder.find_anomalies(word_list, threshold=10.0)
        
        # Should only detect the long word as anomaly
        assert len(anomalies) == 1
        assert anomalies[0]["input_string"] == "verylongwordthatcompresses"
        assert anomalies[0]["ratio"] == 26.0  # 26 chars / 1 token