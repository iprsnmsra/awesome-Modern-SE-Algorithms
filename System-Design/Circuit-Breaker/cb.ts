
enum State { CLOSED, OPEN, HALF_OPEN }

class CircuitBreaker {
    private state: State = State.CLOSED;
    private failureCount: number = 0;
    private readonly failureThreshold: number;
    private readonly cooldownPeriodMs: number;
    private nextAttemptTime: number = 0;

    constructor(threshold: number, cooldownMs: number) {
        this.failureThreshold = threshold;
        this.cooldownPeriodMs = cooldownMs;
    }

    public async execute(action: () => boolean): Promise<string> {
        if (this.state === State.OPEN) {
            if (Date.now() < this.nextAttemptTime) {
                return "FAST_FAIL: Circuit is OPEN";
            }
            this.state = State.HALF_OPEN;
        }

        try {
            const success = action();
            if (!success) throw new Error("Action failed");
            
            this.reset();
            return "SUCCESS";
        } catch (error) {
            this.recordFailure();
            return "FAIL: Action threw an error";
        }
    }

    private recordFailure(): void {
        this.failureCount++;
        if (this.failureCount >= this.failureThreshold) {
            this.state = State.OPEN;
            this.nextAttemptTime = Date.now() + this.cooldownPeriodMs;
        }
    }

    private reset(): void {
        this.failureCount = 0;
        this.state = State.CLOSED;
    }
}

const cb = new CircuitBreaker(2, 100); 
let alwaysFail = () => false;

(async () => {
    await cb.execute(alwaysFail); 
    await cb.execute(alwaysFail); 
    const fastFail = await cb.execute(alwaysFail);
    
    if (fastFail.includes("FAST_FAIL")) {
        console.log("TypeScript Test Passed!");
    } else {
        process.exit(1);
    }
})();