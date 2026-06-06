<div align="center">
  <h1>🌐 Kruskal's Algorithm (Minimum Spanning Tree)</h1>
  <p><b>O(E log E) global network optimization using Union-Find cycle detection.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Core_DSA-red?style=for-the-badge)
</div>

---

**Time Complexity:** O(E log E) *(Dominated by sorting the edges)* **Space Complexity:** O(V + E) *(To store the edges and the Union-Find parent/rank arrays)*

## 🚨 The Problem
You have a set of distributed nodes (cities, servers, power plants) and possible connections between them, each with a cost. You must connect all nodes together so that data/power can flow between any two points, but you have a strictly limited budget. You must find the exact subset of edges that connects everything without any redundant loops (cycles).

## 🧮 The Mathematical Core
A Minimum Spanning Tree (MST) of a connected, undirected, weighted graph is a subset of edges $T$ that connects all vertices $V$ without cycles, such that the total weight $W$ is minimized:

$$W = \sum_{e \in T} w(e)$$

Kruskal's approach is a **Greedy Algorithm** proven optimal by matroid theory. By evaluating edges strictly in ascending order of weight $w(e)$, and rejecting any edge that connects two vertices already in the same connected component, the algorithm avoids local maxima and guarantees a global minimum weight.

## 💡 The Solution
1. **Sort:** Take every edge in the graph and sort them by weight (cheapest to most expensive).
2. **Initialize Union-Find:** Create a Disjoint Set where every node is its own parent.
3. **Iterate & Union:** Loop through the sorted edges. For an edge connecting $U$ and $V$, run `Find(U)` and `Find(V)`. 
   - If the roots are different, they are isolated. Run `Union(U, V)` and add the edge to your MST.
   - If the roots are the same, they are already connected. Skip the edge to prevent a cycle.
4. **Terminate:** Stop the loop the instant you have collected exactly $V - 1$ edges.

## ⚙️ Real-World Use Cases
* **Telecommunications:** Laying out physical network topology (fiber optics, copper wires) to minimize hardware cost.
* **Circuit Design:** Routing traces on a Printed Circuit Board (PCB) to connect pins using the minimum amount of copper.
* **Clustering:** Single-linkage clustering in machine learning (stopping the algorithm early groups data points into distinct clusters).

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for instant CI/CD validation. It includes a highly-optimized, embedded Union-Find class. The test suite builds a 4-node graph, executes Kruskal's, and verifies the total cost of the minimal tree.

* **Python:** `python3 kruskal.py`
* **TypeScript:** `npx ts-node kruskal.ts`
* **C++:** `g++ -std=c++17 kruskal.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not trace a path from start to finish. Sort the pieces by cost, and assemble the cheapest universe."*

**🤫 Secret Principal Engineer Tip:** Sorting edges is the bottleneck $O(E \log E)$. If your edge weights are integers within a small, bounded range (e.g., costs from 1 to 100), you can replace the standard quicksort with **Counting Sort**. This completely shatters the theoretical limit, dropping the sorting phase to $O(E)$, and making the entire algorithm run in nearly linear time!