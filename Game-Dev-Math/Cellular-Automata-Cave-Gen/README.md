<div align="center">
  <h1>⛏️ Cellular Automata Cave Generation</h1>
  <p><b>Simulating natural erosion to generate organic underground networks.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Game_Dev_%26_Math-blue?style=for-the-badge)
</div>

---

**Time Complexity:** O(W x H) *(Per simulation step)* **Space Complexity:** O(W x H) *(Requires a secondary buffer grid during simulation)*

## 🚨 The Problem
Creating random terrain is easy. Creating *playable* random terrain is incredibly difficult. If you generate an underground mining level using pure randomness, the map will be filled with millions of 1x1 disconnected holes. The player will spawn, take two steps, hit a solid wall, and have nowhere to go. You need massive, sprawling, interconnected caverns.

## 💡 The Solution
Cellular Automata treats the map like a living, eroding organism. 
1. **Initial State:** We fill the grid with random noise (usually 45% wall, 55% air).
2. **The Erosion Rule:** We iterate over every cell. We count how many solid walls are in its immediate 3x3 neighborhood. If the neighbor count is strictly greater than 4, the cell becomes a wall. Otherwise, it becomes air.
3. **Iteration:** We swap the buffers and repeat the process 5 times. 

This causes solid blocks to attract other solid blocks, and empty space to attract empty space. The noise "clumps" together into beautiful, smooth caves.

## ⚙️ Real-World Use Cases
* **Procedural Level Design:** *Terraria*, *Spelunky*, and *Deep Rock Galactic* use variations of this math to generate their underground biomes.
* **Fluid Dynamics:** Simulating basic 2D liquid settling in grid-based physics engines.
* **Image Processing:** Used as a noise-reduction pass to remove "salt and pepper" static from binary images.

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for instant CI/CD validation. The code generates a map and prints it directly to the console so you can visually verify the cave structure. (`#` = Wall, `.` = Air).

* **Python:** `python3 cave_gen.py`
* **TypeScript:** `npx ts-node caveGen.ts`
* **C++:** `g++ -std=c++17 cave_gen.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Order naturally arises from chaos, as long as you give it the right rules to live by."*

**🤫 Secret Principal Engineer Tip:** Cellular Automata is great, but it doesn't guarantee *100%* interconnectivity. There might still be an isolated cavern. In production, you must run a **Flood-Fill Algorithm** right after the Automata finishes to identify the "Main Cavern", and then forcefully fill in any disconnected tiny caves with solid rock so the player never spawns out of bounds.

<div align="center">
  <br/>
  <a href="https://ko-fi.com/iprsnmsra"><img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Sponsor Me" /></a>
</div>