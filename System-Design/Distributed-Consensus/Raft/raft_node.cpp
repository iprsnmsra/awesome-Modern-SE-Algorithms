#include <iostream>
#include <cstdlib>
#include <ctime>
#include <cassert>
#include <optional>

using namespace std;

enum class NodeState { FOLLOWER, CANDIDATE, LEADER };

class RaftNode {
private:
    int electionTimeout;
    
    int getRandomTimeout() {
        return 150 + (rand() % 151); // 150 to 300
    }

    void startElection() {
        state = NodeState::CANDIDATE;
        currentTerm++;
        votedFor = nodeId;
        timer = 0;
        electionTimeout = getRandomTimeout();
    }

public:
    int nodeId;
    NodeState state;
    int currentTerm;
    optional<int> votedFor;
    optional<int> leaderId;
    int timer;

    RaftNode(int id) : nodeId(id), state(NodeState::FOLLOWER), currentTerm(0), timer(0) {
        srand(time(nullptr));
        electionTimeout = getRandomTimeout();
    }

    void tick(int deltaMs) {
        if (state == NodeState::LEADER) return;

        timer += deltaMs;
        if (timer >= electionTimeout) {
            startElection();
        }
    }

    bool receiveHeartbeat(int lId, int lTerm) {
        if (lTerm >= currentTerm) {
            state = NodeState::FOLLOWER;
            currentTerm = lTerm;
            leaderId = lId;
            votedFor = nullopt;
            timer = 0;
            return true;
        }
        return false;
    }
};

// --- CI/CD Automated Test ---
int main() {
    RaftNode node(1);
    
    assert(node.state == NodeState::FOLLOWER);
    
    node.tick(400);
    
    assert(node.state == NodeState::CANDIDATE);
    assert(node.votedFor.value() == 1);
    
    bool accepted = node.receiveHeartbeat(2, node.currentTerm + 1);
    
    assert(accepted == true);
    assert(node.state == NodeState::FOLLOWER);
    assert(node.leaderId.value() == 2);
    assert(node.timer == 0);
    
    cout << "C++ Raft Consensus State Machine Test Passed!\n";
    return 0;
}