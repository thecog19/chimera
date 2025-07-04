"""Core Engine for Project Chimera - Comparative Tokenizer Implementation.

This module provides the ComparativeTokenizer class that can load multiple
LLM tokenizers and analyze text strings across different tokenization models.
"""

import json
from typing import Dict, List, Any
import tiktoken
from transformers import AutoTokenizer


class ComparativeTokenizer:
    """A class for comparing tokenization across different LLM tokenizers.
    
    This class loads multiple tokenizers and provides a unified interface
    for analyzing how different models tokenize the same input text.
    """
    
    def __init__(self) -> None:
        """Initialize the ComparativeTokenizer with hardcoded tokenizers.
        
        Currently supports:
        - OpenAI's gpt-4o tokenizer (via tiktoken)
        - Meta's Llama-3-8B tokenizer (via transformers)
        """
        self.tokenizers = {}
        
        # Initialize OpenAI gpt-4o tokenizer
        self.tokenizers["gpt-4o"] = tiktoken.encoding_for_model("gpt-4o")
        
        # Initialize Meta Llama-3-8B tokenizer
        self.tokenizers["Llama-3-8B"] = AutoTokenizer.from_pretrained(
            "meta-llama/Meta-Llama-3-8B-Instruct"
        )
    
    def analyze(self, text_string: str) -> Dict[str, Dict[str, List[Any]]]:
        """Analyze a text string using all loaded tokenizers.
        
        Args:
            text_string: The input text to tokenize and analyze.
            
        Returns:
            A dictionary mapping tokenizer names to their tokenization results.
            Each result contains 'tokens' (list of token strings) and 'ids' 
            (list of token IDs).
        """
        results = {}
        
        # Analyze with gpt-4o tokenizer
        gpt4o_encoding = self.tokenizers["gpt-4o"]
        gpt4o_ids = gpt4o_encoding.encode(text_string)
        gpt4o_tokens = [gpt4o_encoding.decode([token_id]) for token_id in gpt4o_ids]
        
        results["gpt-4o"] = {
            "tokens": gpt4o_tokens,
            "ids": gpt4o_ids
        }
        
        # Analyze with Llama-3-8B tokenizer
        llama_tokenizer = self.tokenizers["Llama-3-8B"]
        llama_ids = llama_tokenizer.encode(text_string)
        llama_tokens = llama_tokenizer.convert_ids_to_tokens(llama_ids)
        
        results["Llama-3-8B"] = {
            "tokens": llama_tokens,
            "ids": llama_ids
        }
        
        return results


if __name__ == "__main__":
    text_to_analyze = "unbelievable SolidGoldMagikarp"
    
    # 1. Initialize the tokenizer engine
    tokenizer_engine = ComparativeTokenizer()
    
    # 2. Analyze the string
    analysis_result = tokenizer_engine.analyze(text_to_analyze)
    
    # 3. Print the results in a readable format
    print(json.dumps(analysis_result, indent=2))