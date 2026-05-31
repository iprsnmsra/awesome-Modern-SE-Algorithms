using System;

public class Program {
    public enum NodeState { FOLLOWER, CANDIDATE, LEADER }

    public class RaftNode {
        public int NodeId;
        public NodeState State;
        public int CurrentTerm;
        public int? VotedFor;
        public int? LeaderId;
        
        private int electionTimeout;
        public int Timer;
        private Random rand = new Random();

        public RaftNode(int nodeId) {
            NodeId = nodeId;
            State = NodeState.FOLLOWER;
            CurrentTerm = 0;
            VotedFor = null;
            LeaderId = null;
            
            electionTimeout = rand.Next(150, 301);
            Timer = 0;
        }

        public void Tick(int deltaMs) {
            if (State == NodeState.LEADER) return;

            Timer += deltaMs;
            if (Timer >= electionTimeout) {
                StartElection();
            }
        }

        private void StartElection() {
            State = NodeState.CANDIDATE;
            CurrentTerm++;
            VotedFor = NodeId;
            Timer = 0;
            electionTimeout = rand.Next(150, 301);
        }

        public bool ReceiveHeartbeat(int leaderId, int leaderTerm) {
            if (leaderTerm >= CurrentTerm) {
                State = NodeState.FOLLOWER;
                CurrentTerm = leaderTerm;
                LeaderId = leaderId;
                VotedFor = null;
                Timer = 0;
                return true;
            }
            return false;
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var node = new RaftNode(1);
        
        if (node.State != NodeState.FOLLOWER) return 1;
        
        node.Tick(400);
        
        if (node.State != NodeState.CANDIDATE || node.VotedFor != 1) return 1;
        
        bool accepted = node.ReceiveHeartbeat(2, node.CurrentTerm + 1);
        
        if (accepted && node.State == NodeState.FOLLOWER && node.LeaderId == 2 && node.Timer == 0) {
            Console.WriteLine("C# Raft Consensus State Machine Test Passed!");
            return 0;
        }
        return 1;
    }
}