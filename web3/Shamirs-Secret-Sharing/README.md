<div align="center">
  <h1>🔐 Shamir's Secret Sharing (SSS)</h1>
  <p><b>Information-theoretic secure key splitting using polynomial interpolation.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Web3_Crypto-gold?style=for-the-badge)
</div>

---

**Time Complexity:** O(K^2) *(For Lagrange Interpolation)* **Space Complexity:** O(N) *(To store the generated shares)*

## 🚨 The Problem
You have a master encryption key. If you store it on one machine, it can be stolen by a single hacker or destroyed in a single server fire. If you copy it to 5 machines for backup, you just increased your risk of theft by 500%. You need a way to distribute the key across multiple geographic locations such that a specific threshold of servers (e.g., 3 out of 5) must cooperate to unlock it, but any less than 3 provides absolutely zero clues about the key.

## 🧮 The Core Logic
The algorithm relies on the fact that it takes $K$ points to define a polynomial of degree $K - 1$.
1. **The Secret:** Convert your secret into a number $S$.
2. **The Polynomial:** Generate a random polynomial of degree $K - 1$:
   
   $$f(x) = S + a_1x + a_2x^2 + \dots + a_{k-1}x^{k-1}$$
   
   (The secret $S$ is intentionally placed at the y-intercept, where $x = 0$).
3. **The Shares:** Evaluate the polynomial at $N$ different points: $(1, f(1)), (2, f(2)), \dots (N, f(N))$. Distribute these $(x, y)$ coordinates to your servers.
4. **The Reconstruction:** When $K$ servers provide their coordinates, use **Lagrange Basis Polynomials** to calculate $f(0)$. The math perfectly intersects the points back to the y-intercept, retrieving $S$.

## ⚙️ Real-World Use Cases
* **Cryptocurrency Custody:** Exchanges like Coinbase split cold-storage wallet keys across multiple executives.
* **DNSSEC:** The master keys that secure the internet's domain name system are split among 7 global security experts using SSS.
* **Zero-Knowledge Architecture:** Distributing trust in Multi-Party Computation (MPC) networks.

## 🚀 Setup & Execution
Built using the **Single-File Architecture**. The test suite splits a secret numeric key into 5 shares with a threshold of 3. It proves that using 3 shares perfectly reconstructs the key, while using only 2 shares generates random garbage.

* **Python:** `python3 shamir_secret.py`
* **TypeScript:** `npx ts-node shamirSecret.ts`
* **C++:** `g++ -std=c++17 shamir_secret.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not cut the map into pieces. Project the map into a higher dimension, and give them the shadows. Only together can they cast the light to reveal the truth."*

**🤫 Secret Principal Engineer Tip:** If you run this algorithm using standard decimals/floats, a hacker with 2 shares can look at the geometry of the curve, guess the trajectory, and narrow down the possibilities. To achieve **perfect information-theoretic security**, Principal Engineers execute all math inside a **Galois Field (Finite Prime Field)**. By applying a modulo of a large Prime Number at every single step, the polynomial geometry wraps around randomly, turning the visual curve into scattered TV static and making geometric guessing mathematically impossible!