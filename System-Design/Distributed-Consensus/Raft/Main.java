import java.util.Random;

public class Main {
    enum NodeState { FOLLOWER, CANDIDATE, LEADER }

    static class RaftNode {
        int nodeId;
        NodeState state;
        int currentTerm;
        Integer votedFor;
        Integer leaderId;
        
        int electionTimeout;
        int timer;
        Random rand = new Random();

        public RaftNode(int nodeId) {
            this.nodeId = nodeId;
            this.state = NodeState.FOLLOWER;
            this.currentTerm = 0;
            this.votedFor = null;
            this.leaderId = null;
            
            this.electionTimeout = rand.nextInt(151) + 150; // 150 to 300
            this.timer = 0;
        }

        public void tick(int deltaMs) {
            if (this.state == NodeState.LEADER) return;

            this.timer += deltaMs;
            if (this.timer >= this.electionTimeout) {
                startElection();
            }
        }

        private void startElection() {
            this.state = NodeState.CANDIDATE;
            this.currentTerm++;
            this.votedFor = this.nodeId;
            this.timer = 0;
            this.electionTimeout = rand.nextInt(151) + 150;
        }

        public boolean receiveHeartbeat(int leaderId, int leaderTerm) {
            if (leaderTerm >= this.currentTerm) {
                this.state = NodeState.FOLLOWER;
                this.currentTerm = leaderTerm;
                this.leaderId = leaderId;
                this.votedFor = null;
                this.timer = 0;
                return true;
            }
            return false;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        RaftNode node = new RaftNode(1);
        
        if (node.state != NodeState.FOLLOWER) System.exit(1);
        
        node.tick(400);
        
        if (node.state != NodeState.CANDIDATE || node.votedFor != 1) System.exit(1);
        
        boolean accepted = node.receiveHeartbeat(2, node.currentTerm + 1);
        
        if (accepted && node.state == NodeState.FOLLOWER && node.leaderId == 2 && node.timer == 0) {
            System.out.println("Java Raft Consensus State Machine Test Passed!");
        } else {
            System.exit(1);
        }
    }
}