#### **1. Description**

As per the Project Chimera design document, the next step is to build our first discovery module. This module will be responsible for automatically identifying strings that are unusually long relative to the number of tokens they generate. This module will consume the `ComparativeTokenizer` engine built in Task 1.

#### **2. Acceptance Criteria**

For this task to be considered complete, the following criteria must be met:

1.  A new file named `compression_analyzer.py` is created inside the `discovery_modules/` directory.
2.  The file must contain a class named `CompressionAnomalyFinder`.
3.  The `__init__` method of the class must accept an instance of `ComparativeTokenizer` as an argument (this is known as dependency injection).
4.  The class must have a public method: `find_anomalies(self, word_list: list[str], threshold: float = 10.0) -> list[dict]`.
5.  The `find_anomalies` method must:
    * Iterate through the provided `word_list`.
    * Use the injected `ComparativeTokenizer` instance to analyze each word.
    * For each tokenizer's result, calculate the ratio: `character_length / token_length`.
    * If the ratio for any tokenizer exceeds the `threshold`, it should record the finding.
6.  The method must return a list of dictionaries. Each dictionary represents a found anomaly and must contain the following keys: `input_string`, `target_tokenizer`, `char_count`, `token_count`, and `ratio`.
7.  A corresponding unit test file, `tests/test_compression_analyzer.py`, must be created.
8.  This test file must contain at least one `pytest` unit test that verifies the functionality of the `CompressionAnomalyFinder`. The test should use a mock or real `ComparativeTokenizer` and assert that a known anomaly is correctly identified and a normal word is correctly ignored.
9.  The `main.py` script should be updated to demonstrate the usage of this new module. It should initialize the `ComparativeTokenizer`, pass it to the `CompressionAnomalyFinder`, and print any found anomalies from a small sample word list.

#### **3. Technical Notes**

* Remember to handle the case where `token_length` is zero to avoid a `ZeroDivisionError`.
* All code must adhere to the **Project Chimera: Python Style Guide**, including PEP 8 compliance, type hinting, and Google-style docstrings.
* The `requirements.txt` file should be updated if any new libraries are introduced (e.g., `pytest`).

