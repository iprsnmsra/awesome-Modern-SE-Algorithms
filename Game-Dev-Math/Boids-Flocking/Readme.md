<div align="center">
  <h1>🦅 Boids Flocking (Swarm Intelligence)</h1>
  <p><b>Emergent AI behavior using 3 simple mathematical rules.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Game_Dev_%26_Math-blue?style=for-the-badge)
</div>

---

**Time Complexity:** O(N^2) naive *(Comparing every boid to every other boid)*.  
**Space Complexity:** O(N) *(Storing the coordinates and velocities of the swarm)*.

## 🚨 The Problem
Animating massive groups of entities (birds, fish, armies) in real-time is computationally impossible if you try to control them from a centralized "Brain." If the server has to calculate exact collision-free paths for 50,000 zerglings, your game will drop to 1 Frame Per Second.

## 💡 The Solution
Invented by Craig Reynolds in 1987, the Boids algorithm proves that complex, beautiful swarm behavior can emerge from strictly local, decentralized rules. Each "Boid" only looks at the other boids within its immediate visual radius and calculates a new velocity vector based on:
1. **Separation:** Vector pointing away from crowded neighbors.
2. **Alignment:** The average velocity vector of the local flock.
3. **Cohesion:** The vector pointing to the average position (center of mass) of the local flock.

## ⚙️ Real-World Use Cases
* **Cinematic VFX:** The massive bat swarms in *Batman Returns* and the Uruk-hai armies in *The Lord of the Rings* were animated using variations of Boids.
* **Autonomous Drones:** Military and commercial drone swarms use these exact rules to fly in formation without crashing.
* **Traffic Simulation:** Modeling highway congestion and self-driving car swarm behavior.

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for instant CI/CD validation. The test suite creates a mini-flock, runs the math simulation for one frame (tick), and verifies that the physics vectors update correctly.

* **Python:** `python3 boids.py`
* **TypeScript:** `npx ts-node boids.ts`
* **C++:** `g++ -std=c++17 boids.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"The flock is not a single organism, but a mathematical negotiation between individuals."*

**🤫 Secret Principal Engineer Tip:** The standard Boids algorithm is O(N^2), meaning 10,000 boids requires 100,000,000 calculations per frame. In an AAA production game engine, you MUST pair this algorithm with a **Spatial Partitioning Grid** or a **Quadtree** to drop the complexity to O(N log N).

<div align="center">
  <br/>
  <a href="https://ko-fi.com/iprsnmsra"><img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Sponsor Me" /></a>
</div>
