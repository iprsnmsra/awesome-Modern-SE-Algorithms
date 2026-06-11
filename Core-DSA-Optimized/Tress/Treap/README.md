<div align="center">
  <h1>🎲 Treap (Tree + Heap)</h1>
  <p><b>O(log N) expected self-balancing tree using randomized priorities.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Core_DSA-red?style=for-the-badge)
</div>

---

**Time Complexity (Search/Insert/Delete):** O(log N) Expected **Space Complexity:** O(N)

## 🚨 The Problem
Self-balancing trees like AVL or Red-Black are notorious for their implementation complexity. Writing bug-free code for their intricate rotation logic and edge cases takes immense effort. While Skip Lists solve this using multiple pointers, they require extra memory overhead. We need a tree structure that is as easy to code as a standard Binary Search Tree but mathematically avoids the worst-case O(N) linear degradation.

## 🧮 The Core Logic
A Treap assigns every node a tuple: $(Key, Priority)$.
* **BST Property:** For any node, all keys in the left subtree are smaller, and all keys in the right subtree are larger.
* **Heap Property:** For any node, its priority is strictly greater than or equal to the priorities of its children.

When you insert a new key, the system assigns it a randomly generated priority. You insert the node following standard BST rules. Then, you look at its parent. If the new node's random priority is higher than the parent's, the Heap Property is violated. You perform a simple Left or Right structural rotation to pull the new node upwards. You repeat this until the Heap Property is restored.

Because priorities are uniformly random, the probability of the tree devolving into a linked list is astronomically low. The expected height of the tree is mathematically proven to be $O(\log N)$.

## ⚙️ Real-World Use Cases
* **Randomized Algorithms:** Used in environments where deterministic behavior is undesirable (preventing malicious users from forcing worst-case O(N) inputs).
* **Implicit Treaps:** An advanced variant used to represent dynamic arrays, allowing operations like "reverse a subarray" or "insert an array into the middle of another" in O(log N) time.
* **Competitive Programming:** The go-to balanced tree because it is drastically faster to implement from scratch than a Red-Black tree.

## 🚀 Setup & Execution
Built using the **Single-File Architecture**. The test suite inserts sequentially ascending data (which would break a normal BST) and mathematically verifies that the tree height remained balanced via randomized rotations.

* **Python:** `python3 treap.py`
* **TypeScript:** `npx ts-node treap.ts`
* **C++:** `g++ -std=c++17 treap.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not try to control the balance. Inject randomness, and the system will balance itself."*

**🤫 Secret Principal Engineer Tip:** While standard Treaps use rotations to maintain balance, the absolute most powerful variant is the **Implicit Treap with Split and Merge**. Instead of rotating, you completely break the tree into two separate trees (Split) and recombine them (Merge) based on keys and priorities. This completely eliminates pointers to parent nodes and makes operations like slicing and concatenating massive datasets incredibly fast!