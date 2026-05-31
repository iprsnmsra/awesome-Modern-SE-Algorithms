import random

class NodeState:
    FOLLOWER = "FOLLOWER"
    CANDIDATE = "CANDIDATE"
    LEADER = "LEADER"

class RaftNode:
    def __init__(self, node_id: int):
        self.node_id = node_id
        self.state = NodeState.FOLLOWER
        self.current_term = 0
        self.voted_for = None
        self.leader_id = None
        
        # Raft uses randomized timeouts (150ms - 300ms) to prevent split votes
        self.election_timeout = random.randint(150, 300)
        self.timer = 0

    def tick(self, delta_ms: int):
        if self.state == NodeState.LEADER:
            # Leaders don't timeout, they send heartbeats
            return

        self.timer += delta_ms
        if self.timer >= self.election_timeout:
            self._start_election()

    def _start_election(self):
        self.state = NodeState.CANDIDATE
        self.current_term += 1
        self.voted_for = self.node_id
        self.timer = 0
        self.election_timeout = random.randint(150, 300)
        # In a full network, we would broadcast RequestVote RPCs here

    def receive_heartbeat(self, leader_id: int, leader_term: int) -> bool:
        # If we see a term greater than or equal to ours, we step down and follow
        if leader_term >= self.current_term:
            self.state = NodeState.FOLLOWER
            self.current_term = leader_term
            self.leader_id = leader_id
            self.voted_for = None
            self.timer = 0 # Reset our election timer!
            return True
        return False # Reject obsolete leaders

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    node = RaftNode(node_id=1)
    
    assert node.state == NodeState.FOLLOWER, "Node should start as Follower"
    
    # Simulate time passing to trigger a timeout
    node.tick(400)
    
    assert node.state == NodeState.CANDIDATE, "Node failed to transition to Candidate on timeout"
    assert node.voted_for == 1, "Candidate must vote for itself"
    
    # Simulate a network event: A different node won the election and sent a heartbeat with a higher term
    accepted = node.receive_heartbeat(leader_id=2, leader_term=node.current_term + 1)
    
    assert accepted == True, "Node rejected a valid higher-term leader"
    assert node.state == NodeState.FOLLOWER, "Node failed to step down gracefully"
    assert node.leader_id == 2, "Node did not recognize the new leader"
    assert node.timer == 0, "Node failed to reset its election timer after heartbeat"
    
    print("Python Raft Consensus State Machine Test Passed!")