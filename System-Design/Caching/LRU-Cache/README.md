# 🧠 LRU (Least Recently Used) Cache

**Time Complexity:** $O(1)$ for both `get()` and `put()`  
**Space Complexity:** $O(C)$ *(where $C$ is the maximum capacity of the cache)*  

## 🚨 The Problem
Your server's RAM is incredibly fast, but highly limited. If your MERN application fetches 10 million user profiles from a slow PostgreSQL database, you want to store them in RAM for instant access next time. But when the RAM fills up, what do you delete? If you use an Array and shift elements down, it costs $O(N)$ time. With 10 million items, your server will freeze every time you add a new one.

## 💡 The Solution
The LRU Cache combines two distinct data structures: a **Hash Map** and a **Doubly Linked List**. 
* The **Hash Map** gives us instant $O(1)$ lookups to find the data.
* The **Doubly Linked List** allows us to instantly rip an item out of the middle and move it to the "Front" (Most Recently Used) in $O(1)$ time without shifting any other data. When the capacity is reached, we simply chop off the "Tail" (Least Recently Used). 

## ⚙️ Real-World Use Cases
*   **Redis / Memcached:** The core memory eviction policy for enterprise caching engines.
*   **React `useMemo` / Browser Engines:** How Chrome manages your local DOM cache and back-button history.
*   **Database Engines:** Managing data pages loaded into memory from the physical hard drive.

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for instant CI/CD validation.

*   **Python:** `python3 lru_cache.py`
*   **TypeScript:** `npx ts-node lruCache.ts`
*   **C++:** `g++ -std=c++17 lru_cache.cpp -o run && ./run`
*   **Java:** `javac Main.java && java Main`
*   **C#:** `dotnet run`

---

> *"There are two hard things in computer science: cache invalidation, naming things, and off-by-one errors."*

**🤫 Secret Principal Engineer Tip:** 
In high-concurrency environments (like a Go or Java backend), a standard LRU Cache will crash if two users read/write at the exact same millisecond. In production, you must wrap the `get` and `put` methods in a `Mutex` (Mutual Exclusion Lock) or a `ReadWriteLock` to make it Thread-Safe.