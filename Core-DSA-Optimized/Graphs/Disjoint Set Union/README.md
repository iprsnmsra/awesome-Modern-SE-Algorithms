<div align="center">
  <h1>🔗 Disjoint Set Union (Union-Find)</h1>
  <p><b>O(1) amortized graph connectivity using Path Compression.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Core_DSA-red?style=for-the-badge)
</div>

---

**Time Complexity:** O(α(N)) amortized practically O(1) *(Where α is the Inverse Ackermann function)* **Space Complexity:** O(N) *(To store the parent and rank arrays)*

## 🚨 The Problem
In massive network graphs (like Facebook's social graph, or routing tables in computer networks), you frequently need to answer the question: *"Is Node A connected to Node B?"* Using standard graph traversal (DFS or BFS) requires iterating through millions of edges every single time a query is made. It is far too slow for real-time systems.

## 💡 The Solution
The Union-Find data structure tracks elements partitioned into a number of disjoint (non-overlapping) sets. It supports two wildly optimized operations:
1. **Find:** Determines which subset an element is in. We use **Path Compression** so that every time `Find` is called, all traversed nodes are re-linked directly to the absolute root of the tree, permanently flattening the structure for all future queries.
2. **Union:** Joins two subsets into a single subset. We use **Union by Rank** to ensure the smaller tree is always attached under the root of the taller tree, preventing the structure from ever devolving into a linked list.

## ⚙️ Real-World Use Cases
* **Network Connectivity:** Quickly checking if two computers are on the same subnet.
* **Kruskal's Algorithm:** The absolute backbone of finding the Minimum Spanning Tree (MST) in a weighted graph.
* **Image Processing:** Connected-component labeling to find distinct objects (like blobs) in computer vision algorithms.

## 🚀 Setup & Execution
Built using the **Single-File Architecture**. The test suite initializes 5 distinct nodes, connects a few of them, and proves that indirect connections are instantly identified while distinct sets remain perfectly isolated.

* **Python:** `python3 union_find.py`
* **TypeScript:** `npx ts-node unionFind.ts`
* **C++:** `g++ -std=c++17 union_find.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not search the path every time. Flatten the path once, and walk it instantly forever."*

**🤫 Secret Principal Engineer Tip:** While textbook Union-Find uses two distinct arrays (`parent` and `rank`), production-grade implementations optimize this into a *single* array. By initializing all elements to `-1`, a negative number tells the algorithm the node is a root, and the absolute value of that number represents the size/rank of the set. Positive numbers represent the index of the parent. This trick cuts your memory footprint exactly in half and drastically reduces CPU cache misses!

<div align="center">
  <br/>
  <a href="https://ko-fi.com/iprsnmsra"><img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Sponsor Me" /></a>
</div>