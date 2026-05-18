# ⭕ Consistent Hashing

**Time Complexity (Lookup):** $O(\log N)$  
**Space Complexity:** $O(V \times S)$ *(Virtual Nodes $\times$ Servers)*  

## 🚨 The Problem
If you scale a database (like Redis or MongoDB) to 10 servers using standard modulo math (`hash(user_id) % 10`), your system works perfectly—until Server 4 crashes. The total server count becomes 9. Suddenly, `hash(user_id) % 9` changes the mathematical location for *every single user*. Your system attempts to migrate terabytes of data across the network instantly, causing a catastrophic cascading failure.

## 💡 The Solution
Consistent Hashing places all servers on a mathematical "Ring" (0 to 360 degrees). When a user's data is hashed, it is placed on the ring, and we simply walk clockwise to find the nearest server. If a server crashes, only the data mapped to that *specific* server moves to the next one. The rest of the network remains completely untouched.

## ⚙️ Real-World Use Cases
*   **Discord / Chat Apps:** Routing millions of concurrent users to the correct WebSocket server.
*   **Netflix / CDN Providers:** Distributing video files across global edge servers.
*   **Amazon DynamoDB:** Under-the-hood data partitioning architecture.

## 🚀 Setup & Execution
This algorithm is built using the **Single-File Architecture**. The CI/CD unit tests are embedded directly inside the main execution block.

*   **Python:** `python3 consistent_hash.py`
*   **TypeScript:** `npx ts-node consistentHash.ts`
*   **C++:** `g++ -std=c++17 consistent_hash.cpp -o run && ./run`
*   **Java:** `javac Main.java && java Main`
*   **C#:** `dotnet run`

---

> *"There are only two hard things in Computer Science: cache invalidation and naming things. And off-by-one errors."* — Phil Karlton

**🤫 Secret Principal Engineer Tip:** 
A basic ring causes uneven data distribution. The code below implements **Virtual Nodes**. We map each server 100 times using slight name variations (e.g., `Server1_0`, `Server1_1`) to ensure perfectly balanced network traffic.

---
⭐ *If this repository helped you understand system design at scale, please leave a Star!*