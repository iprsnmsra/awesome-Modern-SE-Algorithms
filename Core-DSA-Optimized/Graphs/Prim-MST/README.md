<div align="center">
  <h1>🦠 Prim's Algorithm (Minimum Spanning Tree)</h1>
  <p><b>O(E log V) dynamic network expansion using a Min-Heap.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Core_DSA-red?style=for-the-badge)
</div>

---

**Time Complexity:** O(E log V) *(Where E is Edges and V is Vertices)* **Space Complexity:** O(V + E) *(To store the Adjacency List and the Priority Queue)*

## 🚨 The Problem
You need to connect 10,000 servers in a massive data center to a central power grid using the absolute minimum amount of copper wire. The graph is extremely dense (millions of potential connections). If you use Kruskal's Algorithm, sorting millions of edges will consume all available RAM and take too long. You need an algorithm that builds the network dynamically from a single starting point.

## 🧮 The Mathematical Core
Like Kruskal's, Prim's algorithm finds a Minimum Spanning Tree $T$ that minimizes the total weight $W$:

$$W = \sum_{e \in T} w(e)$$

At every step, the graph is divided into two sets: $V_{visited}$ and $V_{unvisited}$. The algorithm mathematically guarantees optimality by always selecting the edge $(u, v)$ such that $u \in V_{visited}$, $v \in V_{unvisited}$, and the edge weight $w(u, v)$ is the absolute minimum available connecting the two sets (the "Cut Property" of graphs).

## 💡 The Solution
1. **The Adjacency List:** We model the graph so each node knows its immediate neighbors.
2. **The Min-Heap:** We maintain a Priority Queue that automatically keeps the cheapest edges at the top.
3. **The Expansion:** We pick Node 0, mark it visited, and push all its edges into the Min-Heap.
4. **The Loop:** We pop the cheapest edge. If it leads to a visited node, we throw it away (cycle prevention). If it leads to an unvisited node, we add it to our MST, mark the node visited, and push all of *its* unvisited neighbors into the heap.

## ⚙️ Real-World Use Cases
* **Data Centers:** Wiring server racks to central switches with minimal cable length.
* **Game Development:** Generating complex, perfect mazes (randomized Prim's algorithm).
* **Traveling Salesperson Approximations:** Prim's MST is used as a baseline to calculate the 2-approximation for the metric TSP problem.

## 🚀 Setup & Execution
Built using the **Single-File Architecture**. The test suite builds a dense graph, executes Prim's, and verifies the total cost of the minimal tree exactly matches the theoretical minimum.

* **Python:** `python3 prim.py`
* **TypeScript:** `npx ts-node prim.ts`
* **C++:** `g++ -std=c++17 prim.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not sort the world. Start where you are, and greedily consume the cheapest path forward."*

**🤫 Secret Principal Engineer Tip:** In academic theory, Principal Engineers are taught to use a **Fibonacci Heap** with Prim's Algorithm to achieve a blistering O(E + V log V) time complexity. However, in real-world production systems (like the Linux Kernel or high-frequency trading), Fibonacci Heaps perform terribly because their complex pointers destroy CPU Cache Locality. Always stick to a standard Binary Min-Heap (arrays) in production—the hardware-level cache hits make it mathematically faster in practice!