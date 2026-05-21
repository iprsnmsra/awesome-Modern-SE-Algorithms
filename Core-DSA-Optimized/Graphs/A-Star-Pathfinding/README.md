<div align="center">
  <h1>🗺️ A* (A-Star) Pathfinding</h1>
  <p><b>Heuristic-driven optimal path routing for Grids and Graphs.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Core_DSA-red?style=for-the-badge)
</div>

---

**Time Complexity:** O(E) in the best case, O(b^d) in the worst case *(where b is the branching factor and d is the depth)*.  
**Space Complexity:** O(V) *(For the Priority Queue and Visited sets)*.

## 🚨 The Problem
Imagine a maze where you are at the bottom-left and the exit is at the top-right. Standard Breadth-First Search (BFS) or Dijkstra's algorithm will explore the bottom-right and top-left corners of the maze equally, wasting massive amounts of memory and time evaluating paths that are obviously going the wrong way. In a high-speed video game with 1,000 NPCs calculating paths 60 times a second, this will freeze your CPU.

## 💡 The Solution
A* uses a scoring system: `F = G + H`
* **G-Cost:** The exact distance from the starting point to the current square.
* **H-Cost (Heuristic):** An estimated distance from the current square to the destination (usually calculated using Manhattan Distance or Euclidean Math).
* **F-Cost:** The total score. 

The algorithm uses a Priority Queue to always explore the square with the lowest F-Cost first. This organically pulls the search algorithm directly toward the target, wrapping tightly around obstacles instead of exploring empty space.

## ⚙️ Real-World Use Cases
* **Game Development:** NPC pathfinding in Unity and Unreal Engine (NavMesh routing).
* **Routing Algorithms:** The foundational logic behind Google Maps and Uber routing.
* **Robotics:** Autonomous vacuum cleaners mapping a living room floor plan.

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for instant CI/CD validation. The code tests a 2D grid maze to prove the algorithm correctly navigates around walls.

* **Python:** `python3 a_star.py`
* **TypeScript:** `npx ts-node aStar.ts`
* **C++:** `g++ -std=c++17 a_star.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"The shortest path between two points is a straight line. But in software, there are always walls in the way."*

**🤫 Secret Principal Engineer Tip:** The choice of your Heuristic function (H) is everything. If you are restricted to moving in 4 directions (up, down, left, right), use **Manhattan Distance**. If you can move in 8 directions (diagonals), use **Chebyshev Distance**. If you use the wrong math, A* degrades and becomes exactly as slow as Dijkstra.