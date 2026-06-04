<div align="center">
  <h1>📉 Bellman-Ford Algorithm</h1>
  <p><b>O(V × E) Single-Source Shortest Path with Negative Weight Cycle Detection.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Core_DSA-red?style=for-the-badge)
</div>

---

**Time Complexity:** O(V × E) *(Where V is Vertices and E is Edges)* **Space Complexity:** O(V) *(To store the distance array)*

## 🚨 The Problem
You are building an arbitrage detection engine for a cryptocurrency exchange. You model the currencies as nodes and the exchange rates as edge weights. To find an arbitrage opportunity, you need to find a path where the total cost drops below zero. Dijkstra's Algorithm fundamentally cannot process negative edge weights and will fail silently.

## 🧮 The Mathematical Core
Bellman-Ford relies on the Principle of Relaxation. For a graph with $V$ vertices, the longest possible shortest path without cycles can contain at most $V-1$ edges. 

The algorithm iterates $V-1$ times. In every iteration, for every edge $(u, v)$ with weight $w$, we evaluate the recurrence relation:

$$dist[v] = \min(dist[v], dist[u] + w)$$

If $dist[u] + w$ is strictly less than the currently known $dist[v]$, we update it. By doing this $V-1$ times, we mathematically guarantee that distance propagates through the longest possible valid path in the graph.

## 💡 The Solution
1. **Initialization:** Set the distance to the source node to $0$, and all other nodes to $\infty$.
2. **Relaxation:** Loop exactly $V-1$ times. Inside the loop, iterate over *every single edge* in the graph and apply the relaxation formula.
3. **Cycle Detection:** Run one final loop over all edges. If any edge can *still* be relaxed ($dist[u] + w < dist[v]$), it mathematically proves the graph contains a Negative Weight Cycle.

## ⚙️ Real-World Use Cases
* **Network Routing:** RIP (Routing Information Protocol) uses a variant of Bellman-Ford to calculate routing tables across the internet.
* **FinTech & Arbitrage:** Detecting infinite-profit loops in currency exchange graphs.
* **Operations Research:** Project scheduling where certain tasks must start a negative amount of time *after* another finishes (leads/lags).

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for instant CI/CD validation. 

* **Python:** `python3 bellman_ford.py`
* **TypeScript:** `npx ts-node bellmanFord.ts`
* **C++:** `g++ -std=c++17 bellman_ford.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Greed blinds you to the bigger picture. True optimization requires evaluating every possibility."*

**🤫 Secret Principal Engineer Tip:** Standard Bellman-Ford always runs exactly $V-1$ times, taking strict $O(V \times E)$ time even if the graph is fully resolved on the 2nd iteration. You must optimize this by adding an `is_updated` boolean flag to the outer loop. If an entire iteration passes without a single edge being relaxed, the graph has reached equilibrium. You can instantly `break` out of the loop early, often dropping real-world execution time from $O(V \times E)$ down to nearly $O(E)$!