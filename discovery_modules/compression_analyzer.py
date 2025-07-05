"""Compression Anomaly Finder for Project Chimera.

This module implements the CompressionAnomalyFinder class which identifies
strings that have unusually high character-to-token compression ratios.
"""

from typing import List, Dict, Any
from src.core_engine import ComparativeTokenizer


class CompressionAnomalyFinder:
    """Identifies strings with unusually high compression ratios.
    
    This class analyzes words to find those that compress into fewer tokens
    than expected based on their character length, which can indicate
    tokenization vulnerabilities.
    """
    
    def __init__(self, tokenizer: ComparativeTokenizer) -> None:
        """Initialize the CompressionAnomalyFinder.
        
        Args:
            tokenizer: An instance of ComparativeTokenizer for analysis.
        """
        self.tokenizer = tokenizer
    
    def find_anomalies(self, word_list: List[str], threshold: float = 10.0) -> List[Dict[str, Any]]:
        """Find words with compression ratios exceeding the threshold.
        
        Args:
            word_list: List of strings to analyze for compression anomalies.
            threshold: The compression ratio threshold above which words are
                flagged as anomalies.
        
        Returns:
            List of dictionaries containing anomaly information. Each dictionary
            has keys: input_string, target_tokenizer, char_count, token_count, ratio.
        """
        anomalies = []
        
        for word in word_list:
            if not word:  # Skip empty strings
                continue
                
            char_count = len(word)
            analysis_result = self.tokenizer.analyze(word)
            
            for tokenizer_name, tokenization_data in analysis_result.items():
                token_count = len(tokenization_data["tokens"])
                
                # Handle zero token count to avoid division by zero
                if token_count == 0:
                    ratio = 0.0
                else:
                    ratio = float(char_count) / token_count
                
                if ratio > threshold:
                    anomalies.append({
                        "input_string": word,
                        "target_tokenizer": tokenizer_name,
                        "char_count": char_count,
                        "token_count": token_count,
                        "ratio": ratio
                    })
        
        return anomalies