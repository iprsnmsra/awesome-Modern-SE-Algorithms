<div align="center">
  <h1>🗺️ Floyd-Warshall Algorithm</h1>
  <p><b>O(V³) Dynamic Programming for the All-Pairs Shortest Path problem.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Core_DSA-red?style=for-the-badge)
</div>

---

**Time Complexity:** O(V³) *(Where V is the number of vertices)* **Space Complexity:** O(V²) *(To store the 2D distance matrix)*

## 🚨 The Problem
If you are building a mapping application for 500 major cities, users want to know the shortest distance between any two cities instantly. If you wait for the user to ask and *then* run a Pathfinding algorithm, it takes too long. You need to pre-compute a massive lookup table containing the shortest distance between *every single pair* of cities. Furthermore, unlike Dijkstra's algorithm, which breaks if a graph has Negative Edge Weights, you need a solution that handles them perfectly.

## 🧮 The Mathematical Core
Floyd-Warshall relies on a fundamental **Dynamic Programming** state transition. For every pair of vertices $(i, j)$ and every possible intermediate vertex $k$, we update the shortest path using the following recurrence relation:

$$dist[i][j] = \min(dist[i][j], dist[i][k] + dist[k][j])$$

* **$dist[i][j]$**: The current known shortest path from source $i$ to destination $j$.
* **$dist[i][k] + dist[k][j]$**: The cost of traveling from $i$ to $k$, and then from $k$ to $j$.

If routing *through* $k$ is strictly cheaper than the direct route, the matrix is updated.

## 💡 The Solution
1. **Initialization:** Create a 2D matrix $V \times V$. Set the distance from any node to itself as $0$. Set all direct edges to their weight, and all unknown paths to $\infty$.
2. **The Triple Loop:** Iterate an intermediate node $k$ from $0$ to $V-1$. For every $k$, iterate through all sources $i$ and all destinations $j$, applying the recurrence relation above.
3. **Negative Cycle Detection:** After completion, check the main diagonal $dist[i][i]$. If any value is strictly less than $0$, a negative weight cycle mathematically exists.

## ⚙️ Real-World Use Cases
* **Network Routing:** OSPF (Open Shortest Path First) routing tables in enterprise Cisco routers.
* **Arbitrage Detection:** In FinTech, detecting negative cycles in currency exchange rates (e.g., USD -> EUR -> JPY -> USD resulting in a net profit).
* **Game Development:** Pre-calculating all possible AI patrol routes in a small, dense level map.

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for instant CI/CD validation. The test suite defines a weighted directed graph, executes the DP algorithm, and verifies the resulting shortest-path matrix.

* **Python:** `python3 floyd_warshall.py`
* **TypeScript:** `npx ts-node floydWarshall.ts`
* **C++:** `g++ -std=c++17 floyd_warshall.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not explore the map. Mathematically fold the map over itself until all distances are minimized."*

**🤫 Secret Principal Engineer Tip:** Floyd-Warshall is the ultimate Negative Cycle detector. After the 3 loops finish, you simply loop through the diagonal of the matrix. The distance from a node to itself should always be 0. If $dist[i][i] < 0$, you have mathematically proven the existence of a Negative Weight Cycle (an infinite loop of decreasing cost)!