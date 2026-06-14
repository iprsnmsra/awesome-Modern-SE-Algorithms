<div align="center">
  <h1>🔤 Byte Pair Encoding (BPE) Tokenizer</h1>
  <p><b>The sub-word tokenization engine powering modern Large Language Models.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-AI_LLM-purple?style=for-the-badge)
</div>

---

**Time Complexity:** O(I * N) *(Where I is the number of merge iterations and N is the number of tokens)* **Space Complexity:** O(N + V) *(Where V is the dynamic vocabulary size)*

## 🚨 The Problem
Computers process numbers, not text. To feed a document into a neural network, we must convert text into integers. 
* **Word Tokenization:** Mapping full words to IDs fails because the system cannot handle slang, typos, or massive vocabularies.
* **Character Tokenization:** Mapping single letters to IDs creates sequence lengths that are too massive for transformer context windows to process efficiently.

We need an algorithm that adaptively bundles repeating character sequences into compact, highly reusable sub-word tokens.

## 🧠 The Core Logic
BPE builds its token vocabulary bottom-up using iterative statistical merges:

1. **Initialization:** Split the target training text into single characters. Append a special end-of-word marker (like `</w>`) to keep track of word boundaries.
2. **Frequency Count:** Scan the entire sequence of tokens and calculate the frequency of every unique adjacent pair (e.g., tracking how often `a` is followed by `t`).
3. **The Merge Rule:** Find the pair with the highest frequency count. Create a brand-new vocabulary entry combining those two tokens.
4. **Substitution:** Replace every occurrence of that specific pair in your text with the new combined token.
5. **Loop:** Repeat this process for a fixed number of iterations or until you hit your target vocabulary size.

## ⚙️ Real-World Use Cases
* **OpenAI GPT Models:** Tiktoken uses a heavily optimized variant of BPE to convert prompts into input vectors.
* **Meta Llama Models:** Employs BPE via SentencePiece to handle multilingual text spaces smoothly.
* **Data Compression:** The original use case of BPE—compressing redundant file strings by substituting common byte patterns.

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for clean deployment. The test suite takes a repetitive training text, runs a series of BPE merge cycles, extracts the learned rules, and encodes an unseen sentence.

* **Python:** `python3 bpe_tokenizer.py`
* **TypeScript:** `npx ts-node bpeTokenizer.ts`
* **C++:** `g++ -std=c++17 bpe_tokenizer.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not dictate vocabulary to an AI. Let the text reveal its own statistical building blocks."*

**🤫 Secret Principal Engineer Tip:** In a naive implementation, searching and replacing character pairs across a massive text sequence takes quadratic time. To achieve blinding speed at scale, production tokenizers maintain an internal **Doubly Linked List** of characters paired with a **Hash Map of Min-Heaps** tracking the positions of every adjacent pair. When a merge occurs, you update pointers locally and update only the neighboring frequencies, dropping the time complexity of a merge step to nearly constant time!