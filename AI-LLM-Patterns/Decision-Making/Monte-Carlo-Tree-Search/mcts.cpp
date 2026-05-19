#include <iostream>
#include <vector>
#include <cmath>
#include <memory>
#include <algorithm>
#include <random>

class GameState {
public:
    int total;
    GameState(int t = 0) : total(t) {}
    std::vector<int> getLegalMoves() const {
        if (total < 5) return {1, 2};
        return {};
    }
    GameState applyMove(int move) const { return GameState(total + move); }
    bool isTerminal() const { return total >= 5; }
    double getResult() const { return total == 5 ? 1.0 : 0.0; }
};

class MCTSNode : public std::enable_shared_from_this<MCTSNode> {
public:
    GameState state;
    std::weak_ptr<MCTSNode> parent;
    int move;
    std::vector<std::shared_ptr<MCTSNode>> children;
    double wins = 0;
    int visits = 0;
    std::vector<int> untriedMoves;

    MCTSNode(GameState s, std::shared_ptr<MCTSNode> p, int m) 
        : state(s), parent(p), move(m) {
        untriedMoves = s.getLegalMoves();
    }

    std::shared_ptr<MCTSNode> uctSelectChild() {
        double c = 1.41;
        std::shared_ptr<MCTSNode> best = nullptr;
        double bestVal = -1.0;
        for (auto& child : children) {
            double uct = (child->wins / child->visits) + c * std::sqrt(std::log(visits) / child->visits);
            if (uct > bestVal) {
                bestVal = uct;
                best = child;
            }
        }
        return best;
    }

    std::shared_ptr<MCTSNode> expand() {
        int m = untriedMoves.back();
        untriedMoves.pop_back();
        auto child = std::make_shared<MCTSNode>(state.applyMove(m), shared_from_this(), m);
        children.push_back(child);
        return child;
    }

    void backpropagate(double result) {
        visits++;
        wins += result;
        if (auto p = parent.lock()) p->backpropagate(result);
    }
};

int runMCTS(GameState rootState, int iterations) {
    auto root = std::make_shared<MCTSNode>(rootState, nullptr, -1);
    std::random_device rd;
    std::mt19937 gen(rd());

    for (int i = 0; i < iterations; i++) {
        auto node = root;
        GameState state = rootState;

        while (node->untriedMoves.empty() && !node->children.empty()) {
            node = node->uctSelectChild();
            state = state.applyMove(node->move);
        }
        if (!node->untriedMoves.empty()) {
            node = node->expand();
            state = state.applyMove(node->move);
        }
        while (!state.isTerminal()) {
            auto moves = state.getLegalMoves();
            std::uniform_int_distribution<> dis(0, moves.size() - 1);
            state = state.applyMove(moves[dis(gen)]);
        }
        node->backpropagate(state.getResult());
    }

    std::shared_ptr<MCTSNode> bestChild = root->children[0];
    for (auto& child : root->children) {
        if (child->visits > bestChild->visits) bestChild = child;
    }
    return bestChild->move;
}

// --- CI/CD Automated Test ---
int main() {
    int optimalMove = runMCTS(GameState(3), 500);
    if (optimalMove == 2) {
        std::cout << "C++ MCTS Test Passed!\n";
        return 0;
    }
    return 1;
}