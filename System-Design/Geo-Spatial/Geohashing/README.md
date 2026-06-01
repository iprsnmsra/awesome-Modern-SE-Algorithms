<div align="center">
  <h1>🌍 Geohashing (Spatial Indexing)</h1>
  <p><b>Converting 2D planetary coordinates into 1D sortable strings for O(1) proximity search.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-System_Design-green?style=for-the-badge)
</div>

---

**Time Complexity:** O(P) *(Where P is the desired string precision/length)* **Space Complexity:** O(P)

## 🚨 The Problem
Imagine you open Uber in New York City. The app needs to find the 5 closest drivers out of 50,000 active drivers in the state. If the app calculates the geometric distance (`sqrt(x^2 + y^2)`) between you and *every single driver* every time you open the app, the servers will melt. Standard databases cannot efficiently index 2D space using 1D B-Trees.

## 💡 The Solution
Geohashing mathematically flattens the earth. 
1. **The Grid:** It divides the world in half horizontally (Latitude) and vertically (Longitude). 
2. **Binary Search:** If you are on the right half, it records a `1`. Left half? `0`. It then recursively divides that half into smaller halves, interleaving the bits (Longitude bit, Latitude bit, Longitude bit...).
3. **Base32 Encoding:** It takes every 5 bits and converts them into a Base32 character (using a custom alphabet that excludes confusing letters like 'a', 'i', 'l', 'o').

**The Result:** A coordinate like `(37.7749, -122.4194)` becomes `9q8yyk8`. 
If your Geohash is `9q8yyk8`, you instantly know that anyone with a Geohash starting with `9q8yy` is standing in the exact same neighborhood as you.

## ⚙️ Real-World Use Cases
* **Ride Sharing (Uber/Lyft):** Finding drivers in your immediate hex-grid or Geohash bucket.
* **Dating Apps (Tinder/Bumble):** Querying users within a 10-mile radius without doing 2D distance math on the entire database.
* **Delivery (DoorDash):** Routing orders to the closest available "Dasher" nodes.

## 🚀 Setup & Execution
Built using the **Single-File Architecture**. The CI/CD test encodes the coordinates of the Golden Gate Bridge and verifies the resulting Geohash exactly matches the mathematical standard.

* **Python:** `python3 geohash.py`
* **TypeScript:** `npx ts-node geohash.ts`
* **C++:** `g++ -std=c++17 geohash.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not calculate distance. Group the world into buckets, and search the bucket."*

**🤫 Secret Principal Engineer Tip:** Geohashing has one major flaw: **The Edge Case**. Two people could be standing 1 meter apart, but if they are standing on the exact mathematical dividing line of the equator or the prime meridian, their Geohashes will be completely different. In production, you must query your own Geohash *plus the 8 surrounding neighbor Geohashes* to guarantee you don't miss anyone.

<div align="center">
  <br/>
  <a href="https://ko-fi.com/iprsnmsra"><img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Sponsor Me" /></a>
</div>