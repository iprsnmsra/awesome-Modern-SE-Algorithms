# 🌳 Merkle Tree (Hash Tree)

**Time Complexity:** $O(N)$ to build, $O(\log N)$ to verify a block  
**Space Complexity:** $O(N)$ *(To store the tree structure)* ## 🚨 The Problem
In distributed systems (like Blockchain, Git, or Peer-to-Peer networks), data is transferred in thousands of tiny chunks from untrusted sources. If one chunk is corrupted or tampered with, you need to identify exactly which piece is broken without re-downloading the entire database. Doing a linear scan of every block is mathematically too slow for global networks.

## 💡 The Solution
A Merkle Tree is a binary tree of hashes. 
1. The bottom "leaf" nodes are hashes of the actual data blocks.
2. Every non-leaf node is a hash of its two child nodes combined.
3. The top "Root Hash" perfectly represents the state of the entire dataset.

If you change even a single character in one data block, its hash changes. This completely changes its parent's hash, which cascades all the way up, completely altering the Root Hash. By comparing hashes down the branches, the network can instantly pinpoint the exact corrupted block in $O(\log N)$ steps.

## ⚙️ Real-World Use Cases
* **Blockchain (Bitcoin/Ethereum):** Allows mobile wallets (SPV nodes) to verify a transaction exists without downloading the 500GB ledger.
* **Git:** Under the hood, Git uses Merkle Trees to track changes in your codebase and instantly see which files were modified.
* **BitTorrent:** Verifying the integrity of file pieces downloaded from random peers.
* **Cassandra / DynamoDB:** "Anti-entropy" repair. Databases use Merkle Trees to quickly figure out which server has outdated data.

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for instant CI/CD validation.

* **Python:** `python3 merkle_tree.py`
* **TypeScript:** `npx ts-node merkleTree.ts`
* **C++:** `g++ -std=c++17 merkle_tree.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Trust, but mathematically verify."*

**🤫 Secret Principal Engineer Tip:** When building a Merkle Tree, if you have an odd number of leaf nodes at any level, the standard protocol (used by Bitcoin) is to simply duplicate the last node and hash it with itself to keep the tree perfectly binary.