<div align="center">
  <h1>🏔️ Perlin Noise (Procedural Generation)</h1>
  <p><b>Gradient noise mathematics for infinite, organic terrain generation.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Game_Dev_%26_Math-blue?style=for-the-badge)
</div>

---

**Time Complexity:** O(1) *(Per coordinate sampled)* **Space Complexity:** O(1) *(Uses a fixed-size permutation array of 512 bytes)*

## 🚨 The Problem
If you are building an infinite open-world game (like *Minecraft* or *No Man's Sky*), you cannot manually 3D-model a planet that is 60 million square kilometers. You have to generate it via code. However, if you use standard pseudo-random number generators (PRNG) like `Math.random()`, the terrain will look like white television static—blocks will alternate wildly between maximum height and minimum depth. It is unplayable.

## 💡 The Solution
Perlin Noise generates "coherent randomness."
1. **The Grid:** It overlays a grid on your 2D or 3D space.
2. **Gradient Vectors:** It assigns a random directional vector to every intersection on the grid using a pre-calculated Permutation Table (so the randomness is identical every time you input the same "Seed").
3. **Interpolation (The Magic):** It calculates the dot product between the grid vectors and your exact coordinate, and smoothly blends them together using a mathematically perfect curve: `6t^5 - 15t^4 + 10t^3`. 

The result is smooth, organic transitions. A high value smoothly rolls down into a low value, naturally creating mountains and valleys.

## ⚙️ Real-World Use Cases
* **Terrain Generation:** *Minecraft* terrain, *Valheim* biomes, and *Starfield* planets.
* **VFX Textures:** Procedurally generating fire, smoke, clouds, and marble textures without using image files.
* **Camera Shake:** Adding organic, realistic "hand-held" camera shake in video editing software (Premiere/After Effects).

## 🚀 Setup & Execution
Built using the **Single-File Architecture**. The CI/CD test samples two coordinates that are close together and verifies that the output smoothly transitions between them.

* **Python:** `python3 perlin.py`
* **TypeScript:** `npx ts-node perlin.ts`
* **C++:** `g++ -std=c++17 perlin.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Nature is not entirely random, nor is it entirely predictable. It sits in the beautiful mathematical space in between."*

**🤫 Secret Principal Engineer Tip:** Classic Perlin Noise creates square-aligned artifacts that are noticeable if you look closely at the terrain. In 2001, Ken Perlin invented an upgraded version called **Simplex Noise**, which uses triangles instead of squares to completely eliminate directional artifacts while calculating faster in higher dimensions!

<div align="center">
  <br/>
  <a href="https://ko-fi.com/iprsnmsra"><img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Sponsor Me" /></a>
</div>