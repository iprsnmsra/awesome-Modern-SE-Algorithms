<div align="center">
  <h1>🧬 KMP String Matching</h1>
  <p><b>Zero-backtracking substring search for massive datasets.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Core_DSA-red?style=for-the-badge)
</div>

---

**Time Complexity:** O(N + M) *(Where N is text length, M is pattern length)* **Space Complexity:** O(M) *(To store the LPS array in memory)*

## 🚨 The Problem
Imagine scanning a 50GB server log file for a highly specific error code pattern: `AABAACAABAA`. Standard search algorithms start at index 0, match a few characters, fail, and then backtrack to index 1 to try again. This constant backtracking means the CPU is reading the same characters thousands of times. On a massive scale (like bioinformatics or log parsing), backtracking is fatal to performance.

## 💡 The Solution
The Knuth-Morris-Pratt algorithm completely eliminates backtracking in the main text.
1. **The LPS Array:** First, it pre-processes the search pattern to find the "Longest Prefix which is also Suffix". 
2. **The Search:** As it scans the main text, if it encounters a mismatch, it checks the LPS array. The array tells the algorithm exactly how many characters it can safely skip forward without missing a potential match. The main text pointer only ever moves to the right.

## ⚙️ Real-World Use Cases
* **Bioinformatics:** Searching for specific DNA/RNA sequences within a human genome.
* **Cybersecurity:** Intrusion Detection Systems (IDS) scanning real-time network packets for virus signatures.
* **Text Editors:** The underlying logic for "Ctrl+F" or "Cmd+F" in highly optimized IDEs.

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for instant CI/CD validation.

* **Python:** `python3 kmp.py`
* **TypeScript:** `npx ts-node kmp.ts`
* **C++:** `g++ -std=c++17 kmp.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"The best way to predict the future is to pre-compute your prefixes."*

**🤫 Secret Principal Engineer Tip:** While KMP is mathematically brilliant, in modern production environments (like the V8 JavaScript engine), developers often use the **Boyer-Moore** algorithm instead for general text search. Boyer-Moore searches from right-to-left and can skip entire words at once. However, KMP remains the undisputed champion when searching highly repetitive data like binary streams or DNA.