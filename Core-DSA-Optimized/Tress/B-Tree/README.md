<div align="center">
  <h1>🗄️ B-Tree (Disk-Optimized Search Tree)</h1>
  <p><b>The massive, wide-node tree architecture that powers modern databases.</b></p>
  
  ![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
  ![Domain](https://img.shields.io/badge/Domain-Core_DSA-red?style=for-the-badge)
</div>

---

**Time Complexity:** O(log N) **Space Complexity:** O(N)

## 🚨 The Problem
RAM (computer memory) is blazing fast, but it is small and loses all data when the power goes out. Hard drives can store terabytes of data permanently, but they are incredibly slow. Every time you ask a hard drive to find a piece of data, it takes a massive time penalty to locate it. If you use a normal, skinny tree to search for a user, you have to jump around the hard drive dozens of times. The database will freeze under heavy traffic.

## 🧠 The Genius (The "Aha!" Moment)
Hard drives do not read one letter at a time. If you ask a hard drive for a single number, it grabs a massive "block" of surrounding data anyway (usually 4,000 bytes at once) and gives it to you. 

The B-Tree exploits this hardware quirk. 
If the hard drive is going to give us 4,000 bytes anyway, **why don't we stuff the tree node with exactly 4,000 bytes worth of keys?** By packing hundreds of keys into a single, massive node, the tree becomes incredibly short and wide. We get hundreds of comparisons for the "price" of a single disk read.

## 💡 The Solution (Step-by-Step)
1. **The Fat Node:** Unlike a normal tree where a node has 1 key and 2 children, a B-Tree node can hold multiple keys (e.g., up to 3 keys) and multiple children (up to 4 children).
2. **The Rules of Order:** Inside the node, the keys are kept perfectly sorted (e.g., `[10, 20, 30]`). 
   * If you are looking for `15`, you look at the keys. It's between `10` and `20`.
   * You follow the child pointer that sits *between* `10` and `20` to go down to the next level.
3. **The Split (Balancing):** You keep inserting numbers into a node until it gets completely full. When it overflows, you crack the node in half! 
   * The left half stays.
   * The right half becomes a new neighbor.
   * The middle number gets kicked *upwards* into the parent node to act as a divider between the two new halves.
4. **Growing Upwards:** Unlike normal trees that grow downwards by adding leaves, a B-Tree perfectly balances itself by cracking and pushing middle numbers upwards. If the absolute top node (the Root) cracks, it pushes a number up to create a brand new Root. The tree grows from the top!

## ⚙️ Real-World Use Cases
* **Relational Databases:** The core storage engine for PostgreSQL, MySQL, and Oracle Database.
* **File Systems:** Mac (APFS), Windows (NTFS), and Linux (Ext4) use B-Trees to keep track of where files are physically located on your hard drive.
* **Search Engines:** Storing massive indexing dictionaries that cannot fit into RAM.

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for instant CI/CD validation. 

* **Python:** `python3 b_tree.py`
* **TypeScript:** `npx ts-node bTree.ts`
* **C++:** `g++ -std=c++17 b_tree.cpp -o run && ./run`
* **Java:** `javac Main.java && java Main`
* **C#:** `dotnet run`

---

> *"Do not fight the hardware. Shape your data to perfectly fit the physical machinery of the disk."*

**🤫 Secret Principal Engineer Tip:** While standard B-Trees are great, production databases like MySQL actually use a slightly upgraded version called the **B+ Tree**. In a standard B-Tree, actual user data is stored everywhere (in the root, in the middle, and at the bottom). In a B+ Tree, the actual user data is *only* stored at the very bottom (the leaves). The top and middle nodes only hold tiny "signpost" numbers to guide you down. This makes the top nodes so incredibly light that you can fit the entire roadmap of a 5-billion-row database directly into your ultra-fast RAM!