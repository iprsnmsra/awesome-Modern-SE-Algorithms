<div align="center">
  <h1>🔏 SHA-256 Cryptographic Hash</h1>
  <p><b>The 64-round bitwise compression engine securing the modern internet.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Web3_Crypto-gold?style=for-the-badge)
</div>

---

**Time Complexity:** O(N) *(Where N is the length of the message)* **Space Complexity:** O(1) *(Operates on fixed 512-bit chunks)*

## 🚨 The Problem
You need a way to take any amount of data—whether it is a 3-letter password or a 100GB 4K movie—and mathematically crush it down into a unique, fixed-size 256-bit signature (a 64-character string). 
1. It must be **Deterministic:** The same file must always produce the exact same hash.
2. It must possess the **Avalanche Effect:** Changing a single pixel in the 100GB movie must completely randomize the resulting 64-character string.
3. It must be **One-Way:** It must be mathematically impossible to reverse-engineer the original file by looking at the hash.

## 🧮 The Core Logic
SHA-256 does not encrypt data; it scrambles it beyond repair using data loss and bitwise logic.

1. **The Padding:** The algorithm takes the raw binary message, appends a single `1` bit, fills the rest with `0`s, and appends the exact length of the original message at the very end. This ensures the data perfectly aligns into 512-bit chunks.
2. **The Message Schedule:** It takes the 512-bit chunk (which is 16 separate 32-bit words) and mathematically stretches it into 64 words using right-rotates (ROTR) and XOR operations.
3. **The Compression Loop:** It initializes 8 registers (`a` through `h`) with specific prime-number constants. It then runs exactly 64 rounds of scrambling. During each round, it calculates two values (`Temp1` and `Temp2`) using logic gates:
   * **Choice (Ch):** If `e`, then `f`, else `g`.
   * **Majority (Maj):** Returns the majority bit of `a`, `b`, and `c`.
   * **Epsilon/Sigma:** Extreme bit-shifting and rotations.
4. **The Avalanche:** The registers are shifted down (`h` becomes `g`, `g` becomes `f`, etc.), and the calculated temporary values are added to the registers using Modulo 2^32 addition. This cascades the bits, ensuring complete structural destruction of the original data.

## ⚙️ Real-World Use Cases
* **Bitcoin Proof-of-Work:** Miners run this exact algorithm trillions of times per second trying to find a hash that starts with a specific number of zeros.
* **Password Storage:** Modern databases store the SHA-256 hash of a password, never the plaintext.
* **Digital Signatures:** Used to hash documents before signing them with ECDSA or RSA keys.

## 🚀 Setup & Execution
Built using the **Single-File Architecture**. This is a pure, zero-dependency, from-scratch implementation of the SHA-256 specification.

* **Python:** `python3 sha256_core.py`
* **TypeScript:** `npx ts-node sha256Core.ts`
* **C++:** `g++ -std=c++17 sha256_core.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not try to hide the data. Scramble its structure so perfectly that the universe itself does not contain enough energy to un-mix the paint."*

**🤫 Secret Principal Engineer Tip:** While SHA-256 is incredibly secure, it suffers from a structural flaw called a **Length Extension Attack**. If a hacker intercepts a hash (e.g., `Hash(Secret + Data)`), the structure of SHA-256 allows them to mathematically append malicious data to the end and generate a perfectly valid new hash `Hash(Secret + Data + Malicious)` *without ever knowing the Secret!* This is exactly why Principal Engineers never use raw SHA-256 for API authentication. They always wrap it in an **HMAC (Hash-based Message Authentication Code)** to neutralize the extension vector!