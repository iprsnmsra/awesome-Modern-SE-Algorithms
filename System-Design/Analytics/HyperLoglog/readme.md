<div align="center">
  <h1>📊 HyperLogLog (HLL)</h1>
  <p><b>O(1) memory probabilistic cardinality estimation for massive datasets.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-System_Design-blue?style=for-the-badge)
</div>

---

**Time Complexity:** O(1) *(per insertion/lookup)* **Space Complexity:** O(1) *(Fixed at ~1.5KB regardless of dataset size)*

## 🚨 The Problem
You need to count the exact number of unique items in a stream of data (e.g., unique IP addresses visiting a website). Storing all the items in a database or a Hash Set requires O(N) memory. If you have 10 billion items, you need over 100 GB of RAM. Distributed systems cannot afford to pass 100 GB of state around just to render a simple "View Count" metric on a dashboard. 

## 🧮 The Core Logic
HyperLogLog does not store the items. It relies on the probability of binary patterns.

1. **The Coin Flip Analogy:** Imagine flipping a coin. Getting a "Heads" is a 50% chance. Getting 5 "Heads" in a row is a (1/2)^5 = 3% chance. If someone tells you they got 5 Heads in a row, you can statistically estimate they must have flipped the coin around 32 times.
2. **The Hash:** HLL hashes every incoming item (e.g., `10.0.0.1` -> `0b1001000...`). The 0s and 1s act as our coin flips.
3. **The Buckets (Registers):** To reduce statistical variance (luck), HLL splits the data into `m` buckets using the first few bits of the hash. 
4. **The Rank:** For the remaining bits, it counts the number of trailing zeros. It stores only the *maximum* number of trailing zeros it has ever seen in that bucket.
5. **The Harmonic Mean:** When you want the total count, HLL calculates the harmonic mean of the values in all buckets and multiplies it by a mathematical constant (`alpha * m^2`) to cancel out extreme outliers. 

## ⚙️ Real-World Use Cases
* **Redis:** The `PFADD` and `PFCOUNT` commands in Redis are powered entirely by HyperLogLog.
* **Database Query Planners:** PostgreSQL uses HLL to quickly estimate table cardinality to determine the fastest `JOIN` strategy.
* **Big Data Analytics:** Hadoop and Apache Spark use HLL to calculate unique metrics across petabytes of log files.

## 🚀 Setup & Execution
Built using the **Single-File Architecture**. This implementation uses an 8-bit bucket size (256 registers, consuming basically zero memory) paired with a 32-bit FNV-1a Hash. It includes Flajolet's "Linear Counting" correction for extreme accuracy on small datasets.

* **Python:** `python3 hyperloglog.py`
* **TypeScript:** `npx ts-node hyperloglog.ts`
* **C++:** `g++ -std=c++17 hyperloglog.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not count the drops in the ocean. Measure the depth of the waves, and let probability reveal the volume."*

**🤫 Secret Principal Engineer Tip:** While standard HyperLogLog is incredible, Google published a paper in 2013 creating **HyperLogLog++**. HLL++ upgrades the hash function from 32-bit to 64-bit to prevent hash collisions on datasets larger than 1 Billion. Furthermore, it uses a "Sparse Representation" where, if the buckets are mostly empty, it compresses them using variable-length encoding, reducing the memory footprint from 1.5KB down to just a few bytes!