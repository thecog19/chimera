"""Main demonstration script for Project Chimera.

This script demonstrates the usage of the ComparativeTokenizer and
CompressionAnomalyFinder modules.
"""

import json
from src.core_engine import ComparativeTokenizer
from discovery_modules.compression_analyzer import CompressionAnomalyFinder


def main() -> None:
    """Demonstrate Project Chimera functionality."""
    print("=== Project Chimera Demo ===\n")
    
    # Initialize the tokenizer engine
    print("1. Initializing ComparativeTokenizer...")
    tokenizer_engine = ComparativeTokenizer()
    
    # Demo basic tokenization
    print("\n2. Basic tokenization analysis:")
    test_string = "unbelievable SolidGoldMagikarp"
    print(f"Analyzing: '{test_string}'")
    
    analysis_result = tokenizer_engine.analyze(test_string)
    print(json.dumps(analysis_result, indent=2))
    
    # Demo compression anomaly detection
    print("\n3. Compression anomaly detection:")
    anomaly_finder = CompressionAnomalyFinder(tokenizer_engine)
    
    # Sample word list with potential anomalies
    sample_words = [
        "hello",
        "world",
        "supercalifragilisticexpialidocious",
        "pneumonoultramicroscopicsilicovolcanoconiosis",
        "antidisestablishmentarianism",
        "testing",
        "compression",
        "tokenization"
    ]
    
    print(f"Analyzing words: {sample_words}")
    print("Threshold: 10.0 (characters per token)")
    
    anomalies = anomaly_finder.find_anomalies(sample_words, threshold=10.0)
    
    if anomalies:
        print(f"\nFound {len(anomalies)} compression anomalies:")
        for i, anomaly in enumerate(anomalies, 1):
            print(f"\n  Anomaly {i}:")
            print(f"    Word: '{anomaly['input_string']}'")
            print(f"    Tokenizer: {anomaly['target_tokenizer']}")
            print(f"    Characters: {anomaly['char_count']}")
            print(f"    Tokens: {anomaly['token_count']}")
            print(f"    Ratio: {anomaly['ratio']:.2f}")
    else:
        print("\nNo compression anomalies found with the current threshold.")
    
    print("\n=== Demo Complete ===")


if __name__ == "__main__":
    main()