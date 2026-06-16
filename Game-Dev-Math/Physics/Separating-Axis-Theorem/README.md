<div align="center">
  <h1>💥 Separating Axis Theorem (SAT)</h1>
  <p><b>The definitive, mathematical algorithm for perfect 2D/3D collision detection.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Game_Dev-green?style=for-the-badge)
</div>

---

**Time Complexity:** O(N + M) *(Where N and M are the number of edges of the two shapes)* **Space Complexity:** O(1)

## 🚨 The Problem
Detecting if two complex geometric shapes are touching is computationally heavy. If you have 10,000 asteroids flying around in a game, checking for collisions between all of them every single frame (60 times a second) will instantly crash a naive physics engine. You need an algorithm that can mathematically prove two objects are *not* touching as fast as humanly possible, so the CPU can move on to the next pair.

## 🧠 The Genius (The "Flashlight" Analogy)
If two objects are not touching, you can draw a straight line between them.
The Separating Axis Theorem states: **If two convex polygons are NOT colliding, there exists an axis onto which their projections will be separate.**

Imagine floating in a dark room with the two shapes and a flashlight.
1. You shine the flashlight from an angle. 
2. You look at the 1D shadow both shapes cast on the wall.
3. If the shadow of Shape A overlaps the shadow of Shape B, they *might* be colliding. Move to the next angle.
4. **The Magic Rule:** If you shine the light and the shadows DO NOT overlap, you immediately stop checking. You have found a gap. They are 100% definitively NOT colliding. 

## 💡 The Solution (Step-by-Step)
Instead of checking infinite flashlight angles, math proves we only need to check the angles that are perfectly perpendicular to the edges of the shapes.
1. **Get the Edges:** Look at every flat side (edge) of Shape A and Shape B.
2. **Find the Axis:** Calculate the "Normal" vector (a line sticking 90 degrees straight out) for each edge. This is our flashlight beam.
3. **Project the Shadows:** Take all the corners of Shape A and calculate where they fall on the Axis line (squashing it into a 1D Min/Max shadow). Do the same for Shape B.
4. **Check for Gap:** If `Max A` is less than `Min B`, or `Max B` is less than `Min A`, you found a gap! Return `False` (No Collision).
5. If you check every single edge of both shapes and never find a gap, they must be colliding. Return `True`.

## ⚙️ Real-World Use Cases
* **Physics Engines:** Box2D (used in Angry Birds) and Havok use SAT to prevent rigid bodies from sinking into each other.
* **Autonomous Vehicles:** Self-driving cars use 3D variants of SAT to calculate bounding-box collisions with surrounding vehicles.
* **UI/UX Design:** Used in canvas-based web apps to determine if a user's custom-drawn selection box overlaps with interactive elements.

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for clean deployment. 

* **Python:** `python3 sat_collision.py`
* **TypeScript:** `npx ts-node satCollision.ts`
* **C++:** `g++ -std=c++17 sat_collision.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"To prove two worlds have collided, you must exhaust every angle of separation. To prove they have not, you only need to find the light shining between them."*

**🤫 Secret Principal Engineer Tip:** SAT only works perfectly on "Convex" shapes (shapes that don't dent inward, like a triangle or hexagon). If you have a "Concave" shape (like a star or a crescent moon), SAT will fail and register false collisions across the empty gaps. To fix this, Principal Engineers run a pre-processing algorithm called **Ear Clipping** to slice the complex concave shape into multiple smaller convex triangles. They then run standard SAT on the grouped triangles!