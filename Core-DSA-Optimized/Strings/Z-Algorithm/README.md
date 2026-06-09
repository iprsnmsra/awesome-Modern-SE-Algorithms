<div align="center">
  <h1>🔤 Z-Algorithm (Linear Pattern Matching)</h1>
  <p><b>Strict O(N + M) substring search using memory-boxes to skip redundant checks.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Core_DSA-red?style=for-the-badge)
</div>

---

**Time Complexity:** O(N + M) *(Where N is text length and M is search word length)* **Space Complexity:** O(N + M) *(To store the Cheat Sheet array)*

## 🚨 The Problem
Imagine you are searching for a 1,000-letter DNA sequence inside a 3-billion-letter genome. A standard search algorithm looks at the first letter, checks the next few, and if it fails, it moves one step forward and starts all over again. If the genome is highly repetitive, the computer ends up re-reading the exact same letters millions of times. It is brutally slow.

## 🧠 The Genius (The "Aha!" Moment)
The Z-Algorithm is built on one brilliant realization: **Never read the same letter twice.**

Imagine your search word is `abacaba`. You are checking the document and successfully match the first 5 letters: `abaca`. But the 6th letter is wrong. 
A normal algorithm abandons the match, goes back to the 2nd letter, and starts over blindly. 
The Z-Algorithm stops and says: *"Wait! I just successfully read `abaca`. I already know exactly what those letters are. I don't need to read them again. I can look at my past notes and instantly skip forward."*

It remembers the "Box" of text it just matched, and if it finds itself inside that Box again, it literally copies its past homework to skip into the future.

## 💡 The Solution (Step-by-Step)
1. **The Setup:** We glue our Search Word and our Document together into one single string. We separate them with a unique divider (like a `#`) so they don't accidentally mix. 
   * *Example:* If we are searching for `apple` inside `redapple`, our new string is: `apple#redapple`.
2. **The Cheat Sheet (Z-Array):** We create an array of numbers. For every single letter in our glued string, we ask: *"Starting from this specific letter, how many characters perfectly match the very beginning of the string?"*
3. **The Memory Box (L, R):** As we read left-to-right to build our Cheat Sheet, we draw a "Box" around the furthest right match we've seen so far.
4. **The Magic Trick:** When we move to the next letter, we check if we are standing *inside* the Memory Box. If we are, we **do not read the text**. We just look at the beginning of our Cheat Sheet and copy the answer we already calculated! We only do manual reading if we step outside the Box.
5. **The Match:** We scan our Cheat Sheet. If we see a number that is exactly equal to the length of our Search Word, we have found a 100% perfect match in the document!

## ⚙️ Real-World Use Cases
* **Bioinformatics:** DNA sequence alignment where absolute precision is required and you cannot afford hashing collisions.
* **Text Editors:** High-speed "Find All" operations in massive log files or codebases (VS Code / Sublime).
* **Data Compression:** Identifying the longest matching prefixes, which is the core engine behind ZIP file compression.

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for instant CI/CD validation. 

* **Python:** `python3 z_algorithm.py`
* **TypeScript:** `npx ts-node zAlgorithm.ts`
* **C++:** `g++ -std=c++17 z_algorithm.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not re-evaluate what you have already observed. Bound your knowledge, and skip into the future."*

**🤫 Secret Principal Engineer Tip:** The standard textbook implementation physically creates a massive new string by gluing the Search Word and the Document together. In production environments with gigabyte-sized log files, allocating that massive new string will cause your server to crash out of memory (OOM). Principal Engineers compute the Z-array "Virtually"—they pass the original Word and Document by reference, and write a smart index-wrapper function that mathematically fakes the glued string without allocating a single extra byte of RAM!