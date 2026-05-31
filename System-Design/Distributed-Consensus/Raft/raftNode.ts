enum NodeState {
    FOLLOWER = "FOLLOWER",
    CANDIDATE = "CANDIDATE",
    LEADER = "LEADER"
}

export class RaftNode {
    public nodeId: number;
    public state: NodeState;
    public currentTerm: number;
    public votedFor: number | null;
    public leaderId: number | null;
    
    private electionTimeout: number;
    public timer: number;

    constructor(nodeId: number) {
        this.nodeId = nodeId;
        this.state = NodeState.FOLLOWER;
        this.currentTerm = 0;
        this.votedFor = null;
        this.leaderId = null;
        
        // Random timeout between 150ms and 300ms
        this.electionTimeout = Math.floor(Math.random() * (300 - 150 + 1) + 150);
        this.timer = 0;
    }

    public tick(deltaMs: number): void {
        if (this.state === NodeState.LEADER) return;

        this.timer += deltaMs;
        if (this.timer >= this.electionTimeout) {
            this.startElection();
        }
    }

    private startElection(): void {
        this.state = NodeState.CANDIDATE;
        this.currentTerm++;
        this.votedFor = this.nodeId;
        this.timer = 0;
        this.electionTimeout = Math.floor(Math.random() * (300 - 150 + 1) + 150);
    }

    public receiveHeartbeat(leaderId: number, leaderTerm: number): boolean {
        if (leaderTerm >= this.currentTerm) {
            this.state = NodeState.FOLLOWER;
            this.currentTerm = leaderTerm;
            this.leaderId = leaderId;
            this.votedFor = null;
            this.timer = 0; // Reset timer
            return true;
        }
        return false;
    }
}

// --- CI/CD Automated Test ---
const node = new RaftNode(1);

if (node.state !== NodeState.FOLLOWER) process.exit(1);

node.tick(400);

if (node.state !== NodeState.CANDIDATE || node.votedFor !== 1) process.exit(1);

const accepted = node.receiveHeartbeat(2, node.currentTerm + 1);

if (accepted && node.state === NodeState.FOLLOWER && node.leaderId === 2 && node.timer === 0) {
    console.log("TypeScript Raft Consensus State Machine Test Passed!");
} else {
    process.exit(1);
}