export class TokenBucket {
    private capacity: number;
    private refillRatePerSecond: number;
    private tokens: number;
    private lastRefillTimestamp: number;

    constructor(capacity: number, refillRatePerSecond: number) {
        this.capacity = capacity;
        this.refillRatePerSecond = refillRatePerSecond;
        this.tokens = capacity;
        this.lastRefillTimestamp = Date.now();
    }

    private refill(): void {
        const now = Date.now();
        // Convert ms to seconds
        const timePassed = (now - this.lastRefillTimestamp) / 1000.0;
        
        const tokensToAdd = timePassed * this.refillRatePerSecond;
        
        if (tokensToAdd > 0) {
            this.tokens = Math.min(this.capacity, this.tokens + tokensToAdd);
            this.lastRefillTimestamp = now;
        }
    }

    public allowRequest(): boolean {
        this.refill();
        
        if (this.tokens >= 1.0) {
            this.tokens -= 1.0;
            return true;
        }
        return false;
    }
}

// --- CI/CD Automated Test ---
async function runTest() {
    const limiter = new TokenBucket(5, 2.0);
    console.log("Simulating a burst of 6 rapid requests...");

    for (let i = 0; i < 5; i++) {
        if (!limiter.allowRequest()) {
            console.error(`Request ${i + 1} was falsely blocked!`);
            process.exit(1);
        }
        console.log(`Request ${i + 1}: Allowed`);
    }

    if (limiter.allowRequest()) {
        console.error("Rate limiter failed to block excess traffic!");
        process.exit(1);
    }
    console.log("Request 6: Blocked (HTTP 429)");

    console.log("Waiting 0.6 seconds for bucket to refill 1 token...");
    await new Promise(resolve => setTimeout(resolve, 600));

    if (!limiter.allowRequest()) {
        console.error("Rate limiter failed to refill!");
        process.exit(1);
    }
    console.log("Request 7: Allowed (After refill)");
    
    console.log("\nTypeScript Token Bucket Rate Limiter Test Passed!");
}

runTest();