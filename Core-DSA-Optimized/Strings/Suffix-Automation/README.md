<div align="center">
  <h1>⚙️ Suffix Automaton (DAWG)</h1>
  <p><b>The ultimate linear-time state machine for indexing all substrings of a text.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Core_DSA-red?style=for-the-badge)
</div>

---

**Time Complexity:** O(N) to build, O(M) to search **Space Complexity:** O(N) *(Strictly bounded to exactly 2N states)*

## 🚨 The Problem
You need to index a massive string of data (like a human genome or a book) so that you can instantly answer complex queries like: "Does this specific pattern exist?", "How many times does it appear?", or "What is the longest common substring between this book and another book?" Building a naive tree of all suffixes takes quadratic memory O(N^2), which is physically impossible for large files.

## 🧠 The Genius (The "Aha!" Moment)
Think of a subway system. If two different train lines eventually go to the exact same final 5 stations, you don't build two separate sets of tracks for those 5 stations. You merge the tracks together! 

A Suffix Automaton does this with text. It recognizes when different prefixes share the exact same future "endings" (suffixes) and mathematically merges their states together. This compression turns an infinite-branching tree into a highly compact, Directed Acyclic Word Graph (DAWG).

## 💡 The Solution (Step-by-Step)
1. **The State Machine:** We build a graph of "States". Every state represents a collection of substrings that all share the exact same occurrences in the text.
2. **The Suffix Link (The Safety Net):** Every state has a special pointer called a "Suffix Link" that points to a smaller, fallback state. If you are reading a word and suddenly hit a dead end, you follow the Suffix Link to instantly fallback to the longest possible valid suffix you were just reading.
3. **Incremental Construction:** We feed the document into the machine one character at a time. The machine dynamically updates, clones states if necessary to split overlapping histories, and redirects its pointers. It builds the entire index in a single left-to-right pass.

## ⚙️ Real-World Use Cases
* **Bioinformatics:** The gold standard for DNA sequence alignment and finding the Longest Common Substring among multiple genomes.
* **Plagiarism Detection:** Instantly identifying massive blocks of copied text across millions of documents.
* **Data Compression:** Identifying repeating patterns for dictionary-based compression algorithms (like LZ77/LZMA).

## 🚀 Setup & Execution
Built using the **Single-File Architecture**. The test suite builds a Suffix Automaton for the string "banana" and validates substring queries in constant time.

* **Python:** `python3 suffix_automaton.py`
* **TypeScript:** `npx ts-node suffixAutomaton.ts`
* **C++:** `g++ -std=c++17 suffix_automaton.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not store every possible future. Store the states, map the transitions, and merge the shared destinies."*

**🤫 Secret Principal Engineer Tip:** The standard way to store state transitions (which character goes to which state) is using a Hash Map. However, Hash Maps have massive memory overhead. If your text only uses standard English letters (a-z), Principal Engineers replace the Hash Map with a simple fixed array of size 26. This transforms the automaton from a fast algorithm into a hardware-accelerated beast, ensuring that every state transition is a single CPU cache-hit!