<div align="center">
  <h1>⚡ Fast Inverse Square Root (0x5F3759DF)</h1>
  <p><b>The legendary Quake III bit-level hack for ultra-fast 3D vector normalization.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Game_Dev-green?style=for-the-badge)
</div>

---

**Time Complexity:** O(1) *(Pure bitwise operations)* **Space Complexity:** O(1)

## 🚨 The Problem
In 3D graphics, to calculate how light bounces off a polygon, you must normalize its normal vector. The formula is $\hat{v} = \frac{\vec{v}}{\sqrt{x^2 + y^2 + z^2}}$. This requires an inverse square root ($1/\sqrt{x}$). In the 1990s and early 2000s, floating-point division and square roots were massively expensive CPU operations. Doing millions of these per frame for dynamic lighting caused catastrophic performance bottlenecks. 

## 🧮 The Core Logic
This algorithm completely bypasses standard arithmetic by exploiting how the IEEE 754 standard stores floating-point numbers in physical memory.

1. **The Evil Bit Hack:** We take a 32-bit floating-point number $x$ and trick the CPU into reading its exact memory address as a 32-bit integer. 
2. **The Magic Number:** By shifting this integer one bit to the right (`>> 1`), we are mathematically dividing the float's exponent by 2 (which is the definition of a square root). We then subtract it from the magic hexadecimal constant `0x5F3759DF`. This miraculously produces an extremely close approximation of $1/\sqrt{x}$.
3. **Newton's Method:** We cast the integer bits back into a float. Because the approximation is slightly off, we run exactly one iteration of the Newton-Raphson method to polish the result:
   
   $$y = y \cdot (1.5 - (x_{half} \cdot y^2))$$

## ⚙️ Real-World Use Cases
* **3D Game Engines:** Quake III Arena used this exact function to calculate dynamic lighting and shadows at 60 FPS on 1999 hardware.
* **Physics Simulators:** Used heavily in custom particle engines where millions of velocities must be normalized simultaneously.
* **Embedded Systems:** Used in microcontrollers and robotics where the CPU lacks a dedicated Floating-Point Unit (FPU) hardware chip for division.

## 🚀 Setup & Execution
Built using the **Single-File Architecture**. 

* **Python:** `python3 fast_inv_sqrt.py`
* **TypeScript:** `npx ts-node fastInvSqrt.ts`
* **C++:** `g++ -std=c++17 fast_inv_sqrt.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not ask the processor for the answer. Rip the bits out of memory, shift the math yourself, and force the hardware to submit."*

**🤫 Secret Principal Engineer Tip:** In modern C++, writing `*(int*)&y` to cast a float to an integer is considered "Undefined Behavior" because it violates Strict Aliasing rules (the compiler might optimize it away entirely). To execute this hack safely in modern production code, you must use `std::memcpy` or `std::bit_cast`. The compiler is smart enough to optimize the `memcpy` entirely out of existence, giving you the exact same blazing speed without angering the memory compiler!