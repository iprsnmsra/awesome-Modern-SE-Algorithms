# 🎲 Monte Carlo Tree Search (MCTS)

**Time Complexity:** Flexible / Time-Bounded *(Runs simulations until time/iterations run out)*  
**Space Complexity:** $O(N)$ *(Where $N$ is the number of nodes expanded in the tree)*  

## 🚨 The Problem
If you are building a complex strategy game (like Go, Chess, or an advanced Unity boss fight), traditional AI uses the Minimax algorithm. Minimax tries to calculate *every* possible future move. In complex games, the number of possible moves exceeds the number of atoms in the universe. The AI will freeze your game engine trying to process turn one.

## 💡 The Solution
MCTS doesn't try to calculate everything. Instead, it plays thousands of completely random games against itself in milliseconds. It uses the **UCT (Upper Confidence Bound applied to Trees)** formula to mathematically balance *Exploitation* (playing moves it knows are good) with *Exploration* (trying unknown moves). It teaches itself the optimal strategy purely through probability. This is the exact algorithm Google DeepMind used to create AlphaGo.

### The UCT Formula
$$UCT = \frac{W_i}{N_i} + c \sqrt{\frac{\ln(N)}{N_i}}$$

## ⚙️ Real-World Use Cases
*   **Game Development:** High-level AI opponents in strategy and board games.
*   **Autonomous Navigation:** Path planning in uncertain environments.
*   **LLM Reasoning:** OpenAI's "Q-Star" / advanced reasoning models use variations of MCTS to plan multi-step logic paths.

## 🚀 Setup & Execution
*   **Python:** `python3 mcts.py`
*   **TypeScript:** `npx ts-node mcts.ts`
*   **C++:** `g++ -std=c++17 mcts.cpp -o run && ./run`
*   **Java:** `javac Main.java && java Main`
*   **C#:** `dotnet run`

---

> *"Intelligence is not about knowing every possible future; it's about making the most statistically sound decision in the present."*

**🤫 Secret Principal Engineer Tip:** 
The exploration parameter ($c$) in the UCT formula is usually set to $\sqrt{2}$ (approx `1.41`). If your AI opponent is too predictable, increase $c$ to force it to try wild, creative strategies. If it's acting too randomly, decrease $c$ to make it ruthlessly exploit known winning moves.

---
⭐ *If this repository helped you level up your AI architecture, please leave a Star!*
