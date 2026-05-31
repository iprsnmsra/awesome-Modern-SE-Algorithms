<div align="center">
  <h1>🗳️ Raft Consensus Algorithm</h1>
  <p><b>Fault-tolerant distributed state machines and leader election.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-System_Design-green?style=for-the-badge)
</div>

---

**Time Complexity:** O(N) *(For broadcast messages across N nodes)* **Space Complexity:** O(L) *(Where L is the length of the replicated log)*

## 🚨 The Problem
In distributed systems, you replicate your data across multiple servers (e.g., Server A, B, and C) so that if one dies, the others take over. But what happens if Server A and B get temporarily disconnected from Server C (a Network Partition)? If a user writes data to Server C, and another user writes conflicting data to Server A, your database is corrupted. This is the "Split-Brain" problem.

## 💡 The Solution
Raft solves this using **Strong Leader Election** and **Quorum (Majority) Voting**.
1. **The Timeout:** Every node has a randomized countdown timer (usually 150ms - 300ms).
2. **The Election:** If a Follower stops hearing heartbeats from the Leader, its timer hits zero. It transitions to a Candidate, votes for itself, and asks the other nodes for votes.
3. **The Quorum:** Because the timeouts are randomized, one node will almost always wake up first, request votes, and win a majority before the others wake up. It becomes the new Leader.
4. **Log Replication:** Only the Leader accepts write requests from clients. It replicates those logs to the Followers. If a network split happens, the smaller side cannot achieve a majority quorum, so it refuses to accept writes, mathematically preventing Split-Brain corruption.

## ⚙️ Real-World Use Cases
* **Kubernetes (etcd):** Kubernetes uses Raft to store the cluster state. If the master node fails, the cluster seamlessly elects a new master.
* **Distributed Databases:** CockroachDB and TiDB use Raft at the storage layer to replicate data across global data centers.
* **Service Discovery:** HashiCorp Consul uses Raft to maintain a highly available registry of microservices.

## 🚀 Setup & Execution
Built using the **Single-File Architecture**. Because we cannot spin up a 5-node TCP network in a single CI/CD file, this code perfectly models the internal **State Machine** of a single Raft Node. The test simulates network ticks, forces a timeout to trigger an election, and then simulates a heartbeat from a higher-term Leader to prove the node yields gracefully.

* **Python:** `python3 raft_node.py`
* **TypeScript:** `npx ts-node raftNode.ts`
* **C++:** `g++ -std=c++17 raft_node.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Consensus is not about agreeing when everything is perfect. It is about agreeing when everything is on fire."*

**🤫 Secret Principal Engineer Tip:** The true genius of Raft is the *randomized* election timeout. Older algorithms like Paxos suffered from "Livelock"—where two nodes wake up at the exact same millisecond, tie the vote, fail, and repeat forever. Raft's random 150-300ms timer completely eliminates Livelock.

<div align="center">
  <br/>
  <a href="https://ko-fi.com/iprsnmsra"><img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Sponsor Me" /></a>
</div>