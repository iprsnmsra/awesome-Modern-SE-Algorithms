<div align="center">
  <h1>🧠 LFU Cache (Least Frequently Used)</h1>
  <p><b>Strict O(1) Memory Eviction using Frequency Mapping and Linked Lists.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Core_DSA-red?style=for-the-badge)
</div>

---

**Time Complexity:** O(1) *(For `get`, `put`, and eviction)* **Space Complexity:** O(C) *(Where C is the maximum capacity of the cache)*

## 🚨 The Problem
LRU (Least Recently Used) caching is flawed for certain workloads. Imagine a Wikipedia article that is viewed 100,000 times a day. If a bot suddenly scans 500 random, obscure articles, those obscure articles will push the popular Wikipedia article out of the LRU cache. When real users return, your database gets hammered with a cache miss for its most popular data.

## 🧮 The $O(1)$ Mathematical Architecture
To evict the least frequently used item in constant time, we must avoid searching for the minimum frequency. We maintain three distinct variables:
1. **`keyToNode` Hashmap:** Maps $Key \rightarrow Node$. Grants $O(1)$ data retrieval.
2. **`freqToList` Hashmap:** Maps $Frequency \rightarrow DoublyLinkedList$. Every node with a frequency of $F$ lives in this list. The list itself is ordered by LRU as a tie-breaker!
3. **`minFreq` Integer:** A simple integer tracking the absolute lowest frequency currently in the cache.

**The Update Logic:** When a node is accessed, its frequency $F$ becomes $F+1$. We sever it from `freqToList[F]` and append it to the head of `freqToList[F+1]`. If `freqToList[F]` becomes completely empty, and $F == minFreq$, we simply increment $minFreq \mathrel{+}= 1$. 

## ⚙️ Real-World Use Cases
* **Content Delivery Networks (CDNs):** Evicting assets based on historical hit-rates rather than just recent spikes.
* **Database Query Planners:** Caching the execution plans of the most heavily executed SQL queries over the lifetime of the server.
* **Web Search Engines:** Keeping the absolute most searched terms (e.g., "weather") permanently in RAM, regardless of temporary trending spikes.

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for instant CI/CD validation. 

* **Python:** `python3 lfu_cache.py`
* **TypeScript:** `npx ts-node lfuCache.ts`
* **C++:** `g++ -std=c++17 lfu_cache.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not let a temporary spike in noise overwrite a lifetime of signal."*

**🤫 Secret Principal Engineer Tip:** The LFU algorithm has one major fatal flaw known as **Cache Pollution**. If an item is accessed 10,000 times in one day, and then never accessed again for 5 years, its frequency is so high that it will *never* be evicted, permanently wasting RAM. In production (like Redis LFU), you must implement **Frequency Decay**—a background thread that halves the frequency of all items every few hours so old trends gradually die off!