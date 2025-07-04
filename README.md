# **Project Chimera: Foundational Design Document**

### **1\. Introduction & Vision**

#### **1.1. The Problem**

Recent experiments have demonstrated that state-of-the-art Large Language Models (LLMs) can convincingly pass conversational Turing Tests. They are capable of generating nuanced emotional responses, forging personal narratives, and performing abstract reasoning, making detection based on conversational content alone unreliable. This presents a significant challenge in security, content moderation, and digital trust.

#### **1.2. The Solution: Attacking the Foundation**

Instead of analyzing the *performance* of a model, which is malleable, we must analyze its fundamental, unchangeable architecture. The most foundational layer of an LLM's text processing is its **tokenizer**. This component translates human-readable strings into a sequence of numerical tokens before the model's "brain" ever sees the input.  
The way a tokenizer segments text is a rigid, algorithmic process that creates predictable quirks and asymmetries. Humans and different LLMs "see" the same string in fundamentally different ways. **Project Chimera** is a tool designed to systematically discover and catalog these asymmetries, creating a database of "fingerprints" that can be used to reliably identify an LLM.

#### **1.3. Project Goals**

* **Primary Goal:** To build an open-source tool that can automatically scan and identify tokenization vulnerabilities and quirks across multiple major LLMs.  
* **Secondary Goal:** To generate a structured, queryable database of these vulnerabilities.  
* **End State:** To provide the foundational data necessary for a "defender" system to craft challenges that can definitively distinguish an LLM from a human in a chat-only environment.

### **2\. System Architecture**

Project Chimera will be composed of four main parts: an **Input Corpus**, a **Core Engine**, pluggable **Discovery Modules**, and a **Vulnerability Database**.

1. **Input Corpus:** A collection of text files (dictionaries, code, common phrases) that serve as the raw material for analysis.  
2. **Core Engine (Comparative Tokenizer):** The heart of the tool. It loads different LLM tokenizers and provides a unified interface for the discovery modules to use.  
3. **Discovery Modules:** Specialized Python scripts that each implement a specific strategy for finding tokenization quirks. They use the Core Engine to process the corpus and identify interesting strings.  
4. **Vulnerability Database:** An SQLite database where the findings from the modules are stored in a structured format for later use.

### **3\. Component Breakdown**

#### **3.1. Core Engine: Comparative Tokenizer**

* **Purpose:** To abstract the complexities of different tokenizer libraries (tiktoken, transformers) into a simple, unified interface.  
* **Functionality:**  
  * Loads tokenizers by their standard identifiers (e.g., gpt-4o, meta-llama/Llama-3-8B-Instruct).  
  * Provides a primary function: analyze(text\_string), which returns a standardized dictionary mapping each tokenizer to its tokenized output (both strings and IDs).

#### **3.2. Discovery Module A: Compression Anomaly Finder**

* **Objective:** To find long character strings that are compressed into a disproportionately small number of tokens. These are often powerful vectors for hiding commands.  
* **Algorithm:**  
  1. Iterate through each word in the input corpus.  
  2. For each word, calculate the ratio: character\_length / number\_of\_tokens.  
  3. If the ratio exceeds a configurable COMPRESSION\_THRESHOLD (e.g., 10.0), it flags the string.  
* **Output:** A database entry with quirk\_type \= "CompressionAnomaly".

#### **3.3. Discovery Module B: Substring Inclusion Detector**

* **Objective:** To find words that, when tokenized, are broken into sub-tokens that are themselves complete, common words. This is a direct vector for embedding hidden commands or triggering unintended associations (e.g., therapist \-\> \['the', 'rapist'\]).  
* **Algorithm:**  
  1. Tokenize a word.  
  2. For each resulting sub-token, check if it exists in a standard English dictionary (excluding single-letter words).  
  3. If a sub-token is a valid word, flag the original string.  
* **Output:** A database entry with quirk\_type \= "SubstringInclusion".

#### **3.4. Discovery Module C: Greedy Merge Analyzer**

* **Objective:** To identify non-intuitive token merging behavior that reveals how a tokenizer prioritizes certain character sequences.  
* **Algorithm:**  
  1. Take two adjacent words from the corpus, WordA and WordB.  
  2. Tokenize WordA and WordB separately.  
  3. Tokenize the concatenated string WordAWordB.  
  4. If the tokenization of the concatenated string is not simply the combined list of the individual word tokens, a "greedy merge" has occurred.  
* **Output:** A database entry with quirk\_type \= "GreedyMerge".

#### **3.5. Vulnerability Database**

* **Technology:** SQLite for portability and ease of use.  
* Schema:  
  | Column Name | Data Type | Description |  
  | :--- | :--- | :--- |  
  | id | INTEGER | Primary Key |  
  | input\_string | TEXT | The string that was flagged |  
  | target\_tokenizer | TEXT | The model/tokenizer that showed the quirk |  
  | tokens\_generated | TEXT | The list of token strings (JSON encoded) |  
  | token\_ids | TEXT | The list of token IDs (JSON encoded) |  
  | quirk\_type | TEXT | Which module found the vulnerability |  
  | notes | TEXT | Field for human analysis and comments |

### **4\. Phase 1: Implementation Roadmap**

1. **Setup:** Initialize a Python project with transformers and tiktoken as dependencies.  
2. **Core Engine:** Build the ComparativeTokenizer class that can load at least two tokenizers (e.g., gpt-4o and Llama-3-8B) and return a comparative analysis for a given string.  
3. **Module Implementation:** Implement the CompressionAnomalyFinder as the first proof-of-concept discovery module.  
4. **Database Integration:** Set up the SQLite database schema and write the functions to log findings from the modules.  
5. **Initial Run:** Execute the tool on a standard English dictionary (/usr/share/dict/words on Linux/macOS) and analyze the initial set of flagged vulnerabilities.