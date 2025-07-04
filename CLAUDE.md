

# Project Chimera: Python Style Guide

Version: 1.1

Purpose: This document provides the official coding standards and best practices for all Python code developed for Project Chimera. Adherence to this guide is mandatory to ensure code quality, readability, and long-term maintainability.


### 1. Core Principle: Readability Counts

All code should be written with the primary goal of being easily understood by other developers. Clean, clear, and self-explanatory code is valued over clever but obscure solutions.


### 2. Formatting and Style


#### 2.1. PEP 8 Compliance

All Python code **must** adhere to the [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/). The standard line length is 88 characters to align with modern formatters like black.


#### 2.2. Naming Conventions



* **Variables & Functions:** Use snake_case (e.g., word_list, analyze_string).
* **Constants:** Use UPPER_SNAKE_CASE (e.g., COMPRESSION_THRESHOLD).
* **Classes:** Use PascalCase (e.g., ComparativeTokenizer).
* **Modules:** Use short, snake_case names (e.g., core_engine.py).


#### 2.3. Docstrings vs. Inline Comments

This project follows a specific philosophy regarding documentation:



* **Docstrings are Mandatory:** Every module, class, and function **must** have a comprehensive docstring explaining its purpose, arguments, and what it returns. We will use the [Google Python Style Guide](https://www.google.com/search?q=https://google.github.io/styleguide/pyguide.html%233.8-comments-and-docstrings) format.
* **Inline Comments Should Be Avoided:** Code should be self-documenting. Instead of writing a comment to explain a complex line of code, refactor the code to be simpler. Avoid obvious comments (e.g., # Increment the counter). Inline comments are only acceptable for explaining non-obvious "why" decisions that cannot be expressed through code alone.

**Example of a good function docstring:**

def calculate_compression_ratio(char_length: int, token_length: int) -> float: \
    """Calculates the character-to-token compression ratio. \
 \
    Args: \
        char_length: The total number of characters in the string. \
        token_length: The total number of tokens generated from the string. \
 \
    Returns: \
        The compression ratio as a float. Returns 0.0 if token_length is zero \
        to prevent division by zero errors. \
    """ \
    if token_length == 0: \
        return 0.0 \
    return float(char_length) / token_length \



#### 2.4. Type Hinting

All function signatures and variable declarations **must** include type hints as specified in [PEP 484](https://www.python.org/dev/peps/pep-0484/). This is critical for static analysis and code clarity.


### 3. Project Structure and Practices


#### 3.1. Dependencies

All project dependencies must be listed in a requirements.txt file in the root of the repository.


#### 3.2. Logging

Use the built-in logging module for any diagnostic output. Do not use print() statements in library code. print() is only acceptable in the main execution block (if __name__ == "__main__":) for demonstrating functionality.


#### 3.3. Error Handling

Use specific exceptions where possible (e.g., FileNotFoundError instead of a generic Exception). All file operations or API calls must be wrapped in try...except blocks.


#### 3.4. File Structure

Each distinct class or major component should reside in its own Python file. For example:

/project_chimera/ \
|-- main.py \
|-- core_engine.py \
|-- discovery_modules/ \
|   |-- __init__.py \
|   |-- compression_analyzer.py \
|   |-- substring_analyzer.py \
|-- tests/ \
|   |-- test_core_engine.py \
|   |-- test_compression_analyzer.py \
|-- requirements.txt \



#### 3.5. Unit Testing



* **Framework:** All unit tests **must** be written using the pytest framework.
* **Location:** Tests must be placed in a top-level /tests directory that mirrors the project's package structure.
* **Requirement:** All new functionality (classes, functions) must be accompanied by corresponding unit tests. The goal is to maintain high code coverage and ensure that all components are independently verifiable.
* **Execution:** Tests should be runnable from the root directory with a single pytest command.

This style guide will serve as our single source of truth for code quality. Claude should adhere to these standards in all submitted code, and my reviews will be conducted against this document.
