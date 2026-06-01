<div align="center">
  <h1>❄️ Snowflake IDs (Distributed ID Generation)</h1>
  <p><b>Chronological, highly-scalable 64-bit unique identifiers.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-System_Design-green?style=for-the-badge)
</div>

---

**Time Complexity:** O(1) *(Bitwise shifts execute in nanoseconds)* **Space Complexity:** O(1) *(Requires zero memory overhead)*

## 🚨 The Problem
In a microservices architecture processing 50,000 requests per second (like creating Tweets or Discord messages), you cannot rely on a single SQL database to assign sequential IDs (`id=1`, `id=2`). The database will lock and crash. UUIDs (`550e8400-e29b-41d4-a716-446655440000`) solve the collision problem, but they are 128-bit strings, which causes heavy fragmentation in B-Tree database indexes and ruins chronological sorting.

## 💡 The Solution
Invented by Twitter, the Snowflake algorithm generates a mathematically perfect 64-bit integer entirely in local server memory.

**The 64-bit Breakdown:**
* `1 bit`: Sign bit (always 0, ensures the ID is a positive integer).
* `41 bits`: Timestamp (Milliseconds since a custom epoch. Lasts for 69 years).
* `5 bits`: Datacenter ID (Supports 32 datacenters).
* `5 bits`: Worker/Machine ID (Supports 32 machines per datacenter).
* `12 bits`: Sequence Number (Allows 4,096 unique IDs to be generated *in the exact same millisecond* on the exact same machine).

Because the highest bits represent the timestamp, Snowflake IDs are "k-sortable" (chronological).

## ⚙️ Real-World Use Cases
* **Twitter / X:** Primary keys for all Tweets.
* **Discord:** Primary keys for all Messages, Users, and Channels. (Discord modified it slightly to use a custom epoch of 2015).
* **Instagram:** Sharded database indexing (Instagram uses a modified Snowflake implementation stored in PL/pgSQL).

## 🚀 Setup & Execution
Built using the **Single-File Architecture**. The CI/CD test forces the generation of two IDs in rapid succession, proves they are unique, and mathematically verifies that the second ID is strictly greater than the first (chronological sorting).

* **Python:** `python3 snowflake.py`
* **TypeScript:** `npx ts-node snowflake.ts`
* **C++:** `g++ -std=c++17 snowflake.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not ask the database for an identity. Calculate it yourself."*

**🤫 Secret Principal Engineer Tip:** The deadliest edge case in this algorithm is **NTP Clock Drift** (when a server's internal clock accidentally moves backward to sync with global time). If the clock moves backward, the algorithm will generate duplicate IDs. A production-grade Snowflake generator *must* contain an exception that freezes the generator if `current_time < last_time`.

<div align="center">
  <br/>
  <a href="https://ko-fi.com/iprsnmsra"><img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Sponsor Me" /></a>
</div>