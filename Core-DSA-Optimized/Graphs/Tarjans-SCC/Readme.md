# 🕸️ Tarjan's Strongly Connected Components (SCC)

**Time Complexity:** $O(V + E)$ *(Vertices + Edges: Touches every node exactly once)*  
**Space Complexity:** $O(V)$ *(For the internal Stack and State Arrays)*  

## 🚨 The Problem
Imagine a social network with 1 Billion users, or an NPM `package.json` with 10,000 dependencies. You need to find all the tight-knit "clusters" (where everyone follows everyone, or packages that circularly depend on each other). If a junior engineer runs a standard BFS/DFS from *every single node* to map the connections, the time complexity is $O(V \times (V+E))$. The server will melt down before it finishes calculating.

## 💡 The Solution
Robert Tarjan invented a genius way to find every cluster in exactly **one continuous pass**. As the Depth-First Search dives into the graph, it assigns an `ID` to each node and tracks a `low-link` value (asking: *"What is the oldest ancestor I can circle back to?"*). By pushing nodes onto a Stack, it instantly groups millions of nodes into perfect clusters the moment a "dead end" is reached. 

## ⚙️ Real-World Use Cases
*   **Package Managers (npm, yarn):** Detecting circular dependencies that would break a build.
*   **Database Engines:** Detecting deadlocks (when Transaction A waits for B, and B waits for A).
*   **Social Networks:** Clustering tightly-knit friend groups for recommendation engines.

## 🚀 Setup & Execution
Built using the **Single-File Architecture** for instant CI/CD validation.

*   **Python:** `python3 tarjan_scc.py`
*   **TypeScript:** `npx ts-node tarjanScc.ts`
*   **C++:** `g++ -std=c++17 tarjan_scc.cpp -o run && ./run`
*   **Java:** `javac Main.java && java Main`
*   **C#:** `dotnet run`

---

> *"Good algorithms are discovered. Great algorithms are born out of absolute necessity."*

**🤫 Secret Principal Engineer Tip:** 
In an interview, they might ask you to compare Tarjan's to **Kosaraju's Algorithm**. The answer is simple: Kosaraju requires you to traverse the entire graph *twice* (and reverse all the edges). Tarjan does it in a single pass. Tarjan is practically always faster in real-world memory caches.
