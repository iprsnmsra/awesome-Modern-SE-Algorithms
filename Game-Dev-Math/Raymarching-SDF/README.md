<div align="center">
  <h1>🔦 Raymarching with SDFs</h1>
  <p><b>Procedural 3D rendering using Signed Distance Fields.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Game_Dev_%26_Math-blue?style=for-the-badge)
</div>

---

**Time Complexity:** O(R x S) *(Where R is the number of rays/pixels, and S is the max steps per ray)* **Space Complexity:** O(1) *(Pure mathematics, zero 3D meshes stored in memory)*

## 🚨 The Problem
Rendering volumetric elements like clouds, fog, or infinitely repeating fractal geometry (like the Mandelbulb) is computationally impossible using standard polygon rendering. Triangles cannot smoothly blend into one another like liquid drops, and storing infinite geometry will instantly crash your RAM.

## 💡 The Solution
Raymarching flips 3D rendering on its head. There are no polygons. The entire 3D world is defined by a mathematical function called a **Signed Distance Field (SDF)**. 
1. **The March:** A ray is cast from the camera. We evaluate the SDF to find the distance to the absolute closest object in the scene.
2. **The Safe Step:** Because we know nothing is closer than that distance, we safely move the ray forward by exactly that amount.
3. **The Hit:** We repeat this step until the SDF returns a distance of roughly `0.001` (meaning we touched the surface) or we exceed our maximum render distance (meaning we hit the skybox).

## ⚙️ Real-World Use Cases
* **Unreal Engine 5 (Lumen/Nanite):** UE5 heavily relies on hardware Raymarching and SDFs for its revolutionary global illumination and infinite detail rendering.
* **The Demoscene (Shadertoy):** Creating mind-bending 3D graphics in a 4-kilobyte executable file by defining the entire game world in a single mathematical shader.
* **Medical Imaging:** Rendering MRI and CT scan volumetric data without converting it to heavy 3D meshes.

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for instant CI/CD validation. The test suite fires a mathematical ray at a procedural sphere to verify the marching algorithm calculates the exact distance to impact.

* **Python:** `python3 raymarch.py`
* **TypeScript:** `npx ts-node raymarch.ts`
* **C++:** `g++ -std=c++17 raymarch.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not ask where the polygon is. Ask how far you are from the math."*

**🤫 Secret Principal Engineer Tip:** The true magic of SDFs is **Smooth Minimums**. If you have two spheres intersecting, you can use a smooth-min mathematical function (`smin`) to seamlessly blend them together like liquid mercury. This is impossible with standard polygonal raytracing!

<div align="center">
  <br/>
  <a href="https://ko-fi.com/iprsnmsra"><img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Sponsor Me" /></a>
</div>