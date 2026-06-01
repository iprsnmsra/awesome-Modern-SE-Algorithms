public class Main {
    static class TokenBucket {
        private final double capacity;
        private final double refillRatePerSecond;
        private double tokens;
        private long lastRefillTimestamp;

        public TokenBucket(double capacity, double refillRatePerSecond) {
            this.capacity = capacity;
            this.refillRatePerSecond = refillRatePerSecond;
            this.tokens = capacity;
            this.lastRefillTimestamp = System.currentTimeMillis();
        }

        private void refill() {
            long now = System.currentTimeMillis();
            double timePassed = (now - lastRefillTimestamp) / 1000.0;
            
            double tokensToAdd = timePassed * refillRatePerSecond;
            
            if (tokensToAdd > 0) {
                tokens = Math.min(capacity, tokens + tokensToAdd);
                lastRefillTimestamp = now;
            }
        }

        public synchronized boolean allowRequest() {
            refill();
            
            if (tokens >= 1.0) {
                tokens -= 1.0;
                return true;
            }
            return false;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) throws InterruptedException {
        TokenBucket limiter = new TokenBucket(5.0, 2.0);
        System.out.println("Simulating a burst of 6 rapid requests...");

        for (int i = 0; i < 5; i++) {
            if (!limiter.allowRequest()) {
                System.err.println("Request " + (i + 1) + " was falsely blocked!");
                System.exit(1);
            }
            System.out.println("Request " + (i + 1) + ": Allowed");
        }

        if (limiter.allowRequest()) {
            System.err.println("Rate limiter failed to block excess traffic!");
            System.exit(1);
        }
        System.out.println("Request 6: Blocked (HTTP 429)");

        System.out.println("Waiting 0.6 seconds for bucket to refill 1 token...");
        Thread.sleep(600);

        if (!limiter.allowRequest()) {
            System.err.println("Rate limiter failed to refill!");
            System.exit(1);
        }
        System.out.println("Request 7: Allowed (After refill)");
        
        System.out.println("\nJava Token Bucket Rate Limiter Test Passed!");
    }
}