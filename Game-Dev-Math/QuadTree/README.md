<div align="center">
  <h1>🌳 Quadtree Spatial Partitioning</h1>
  <p><b>High-performance 2D spatial indexing for collision detection.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Game_Dev_%26_Math-blue?style=for-the-badge)
</div>

---

**Time Complexity:** O(log N) for Insertion and Querying.  
**Space Complexity:** O(N) *(To store the points and the tree structure)*.

## 🚨 The Problem
You are building a 2D battle royale game with 1,000 players firing bullets. To check if a bullet hit someone, you have to check the bullet's coordinate against every single player's coordinate. 1,000 players * 1,000 bullets = 1,000,000 math operations every single frame. At 60 frames per second, your CPU will melt trying to process 60 million collision checks.

## 💡 The Solution
A Quadtree is a spatial data structure that recursively divides a 2D space into four quadrants (Northwest, Northeast, Southwest, Southeast). 
1. **Capacity:** Each quadrant has a strict capacity (e.g., max 4 points).
2. **Subdivision:** If a 5th point is added, the quadrant splits into 4 smaller sub-quadrants and redistributes the points.
3. **Querying:** When a bullet is fired, we create a small "Query Boundary" around the bullet. The tree instantly discards any major quadrants that don't intersect the bullet's area, drilling down in O(log N) time to return only the 2 or 3 players actually standing near the bullet.

## ⚙️ Real-World Use Cases
* **Game Engines (Unity/Godot):** 2D collision detection and physics culling.
* **Rendering:** Frustum culling (only rendering the trees and rocks that the player's camera is currently looking at).
* **Maps (Google Maps):** Fetching the nearest restaurants within a 5-mile radius of your GPS coordinate without scanning the entire global database.

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for instant CI/CD validation. The test suite inserts points, queries a specific region, and verifies that the tree instantly rejects points outside the boundary.

* **Python:** `python3 quadtree.py`
* **TypeScript:** `npx ts-node quadtree.ts`
* **C++:** `g++ -std=c++17 quadtree.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not search the world. Divide the world, and let the space search itself."*

**🤫 Secret Principal Engineer Tip:** Quadtrees are for 2D space. If you are building a 3D game in Unreal Engine, you upgrade this exact algorithm to an **Octree** (which divides space into 8 cubes instead of 4 squares). For massive, open-world 3D environments, modern AAA engines often use a **Bounding Volume Hierarchy (BVH)** tree.

<div align="center">
  <br/>
  <a href="https://ko-fi.com/iprsnmsra"><img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Sponsor Me" /></a>
</div>