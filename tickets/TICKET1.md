### **Task 1: Build the Core Engine (`ComparativeTokenizer`)**

**To Claude:**

Your first task is to build the foundational component of Project Chimera as outlined in the design document. We need a stable, reliable Core Engine before we can build any discovery modules.

**Objective:** Create a Python class named `ComparativeTokenizer` that can load multiple specified LLM tokenizers and use them to analyze a given text string.

**Key Requirements:**

1.  The script should define a class named `ComparativeTokenizer`.
2.  The `__init__` method should initialize and store the tokenizers we want to test. For this first version, please hardcode the following two:
      * OpenAI's `gpt-4o` tokenizer (using the `tiktoken` library).
      * Meta's `Llama-3-8B` tokenizer (using the `transformers` library).
3.  Create a public method `analyze(self, text_string)`.
4.  This `analyze` method must take a string as input and return a dictionary. The dictionary keys should be the tokenizer names, and the values should be another dictionary containing the list of token strings and the list of token IDs.
5.  Ensure all necessary libraries (`transformers`, `tiktoken`) are imported.

**Example Usage & Expected Output:**

Please include a main execution block (`if __name__ == "__main__":`) to demonstrate its functionality.

```python
# Example of how the class should be used
if __name__ == "__main__":
    text_to_analyze = "unbelievable SolidGoldMagikarp"
    
    # 1. Initialize the tokenizer engine
    tokenizer_engine = ComparativeTokenizer()
    
    # 2. Analyze the string
    analysis_result = tokenizer_engine.analyze(text_to_analyze)
    
    # 3. Print the results in a readable format
    import json
    print(json.dumps(analysis_result, indent=2))

# Expected output structure from the print statement:
# {
#   "gpt-4o": {
#     "tokens": ["un", "believ", "able", " Solid", "Gold", "Mag", "ik", "arp"],
#     "ids": [539, 2 believable, 2893, 1 solid, 1 gold, 1 mag, 1 ik, 1 arp]
#   },
#   "Llama-3-8B": {
#     "tokens": ["unbelievable", " Solid", "Gold", "Mag", "ik", "arp"],
#     "ids": [1 unbelievable, 1 solid, 1 gold, 1 mag, 1 ik, 1 arp]
#   }
# }
# (Note: The exact tokens and IDs are illustrative and may vary)
```