<div align="center">
  <h1>🔴⚫ Red-Black Tree</h1>
  <p><b>O(log N) self-balancing binary search tree using color-coded rotation invariants.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Core_DSA-red?style=for-the-badge)
</div>

---

**Time Complexity (Search/Insert/Delete):** O(log N) **Space Complexity:** O(N)

## 🚨 The Problem
Data often arrives sorted or nearly sorted. If you insert sorted data into a standard Binary Search Tree, it forms a straight line. To fix this, AVL Trees were invented, which enforce perfect mathematical balance. However, AVL Trees are *too* strict. They require so many structural rotations during `Insert` and `Delete` operations that write-heavy databases suffer severe performance penalties. We need a tree that is balanced *enough* for fast searches, but relaxed *enough* for fast writes.

## 🧮 The Core Logic
A Red-Black Tree guarantees that no path from the root to a leaf is more than twice as long as any other path. It achieves this by enforcing 5 immutable invariants:

1. Every node is either **Red** or **Black**.
2. The root is always **Black**.
3. Every `NULL` leaf is considered **Black**.
4. If a node is **Red**, both of its children must be **Black** (No two consecutive Red nodes).
5. Every path from a given node to any of its descendant `NULL` leaves must contain exactly the same number of **Black** nodes.

Because of these rules, the maximum height of the tree is strictly bounded. **In simple terms: the height of the tree will never exceed twice the base-2 logarithm of the total number of nodes.** This guarantees that the tree will never degrade into a linked list, locking in optimal search speeds no matter how the data is inserted.

## 💡 The Solution
1. **Insertion:** Every new node is initially painted **Red**. We insert it exactly like a standard BST.
2. **The Fix-Up Engine:** If inserting the Red node violates Rule 4 (its parent is also Red), the engine activates.
3. **The Uncle:** The engine looks at the newly inserted node's "Uncle" (the sibling of its parent). 
   - If the Uncle is **Red**, we simply flip the colors of the Parent, Uncle, and Grandparent.
   - If the Uncle is **Black**, we execute precise geometric **Rotations** (Left or Right) and swap colors to restore the invariants.

## ⚙️ Real-World Use Cases
* **Standard Libraries:** The engine behind C++ `std::map`/`std::set` and Java `TreeMap`/`TreeSet`.
* **Linux Kernel:** The Completely Fair Scheduler (CFS) uses a Red-Black Tree to track and allocate CPU time slices to active processes.
* **Database Indexing:** Used in in-memory databases where fast writes and fast reads must be perfectly balanced.

## 🚀 Setup & Execution
Built using the **Single-File Architecture**. The test suite inserts sequentially ascending data (which would break a normal BST) and mathematically verifies that the tree height remained balanced via rotations.

* **Python:** `python3 red_black_tree.py`
* **TypeScript:** `npx ts-node redBlackTree.ts`
* **C++:** `g++ -std=c++17 red_black_tree.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Perfect balance is too expensive to maintain. Bound the chaos, rotate the extremes, and speed will follow."*

**🤫 Secret Principal Engineer Tip:** In a naive implementation, storing the "Color" of a node requires adding a `boolean` to the struct/class. Because of memory alignment padding in C++ and Java, that single boolean will bloat your node size by up to 8 extra bytes! To fix this, Principal Engineers use **Pointer Tagging**. On 64-bit systems, memory pointers are 8-byte aligned, meaning the lowest 3 bits of a pointer are *always* `000`. You can store the Red/Black color bit directly inside the lowest bit of the `parent` pointer, saving massive amounts of RAM and vastly improving CPU Cache hits!