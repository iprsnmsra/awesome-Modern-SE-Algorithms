using System;
using System.Threading;

public class Program {
    public class TokenBucket {
        private readonly double capacity;
        private readonly double refillRatePerSecond;
        private double tokens;
        private long lastRefillTimestamp;
        private readonly object _lock = new object();

        public TokenBucket(double capacity, double refillRatePerSecond) {
            this.capacity = capacity;
            this.refillRatePerSecond = refillRatePerSecond;
            this.tokens = capacity;
            this.lastRefillTimestamp = Environment.TickCount64;
        }

        private void Refill() {
            long now = Environment.TickCount64;
            double timePassed = (now - lastRefillTimestamp) / 1000.0;
            
            double tokensToAdd = timePassed * refillRatePerSecond;
            
            if (tokensToAdd > 0) {
                tokens = Math.Min(capacity, tokens + tokensToAdd);
                lastRefillTimestamp = now;
            }
        }

        public bool AllowRequest() {
            lock (_lock) {
                Refill();
                
                if (tokens >= 1.0) {
                    tokens -= 1.0;
                    return true;
                }
                return false;
            }
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var limiter = new TokenBucket(5.0, 2.0);
        Console.WriteLine("Simulating a burst of 6 rapid requests...");

        for (int i = 0; i < 5; i++) {
            if (!limiter.AllowRequest()) {
                Console.WriteLine($"Request {i + 1} was falsely blocked!");
                return 1;
            }
            Console.WriteLine($"Request {i + 1}: Allowed");
        }

        if (limiter.AllowRequest()) {
            Console.WriteLine("Rate limiter failed to block excess traffic!");
            return 1;
        }
        Console.WriteLine("Request 6: Blocked (HTTP 429)");

        Console.WriteLine("Waiting 0.6 seconds for bucket to refill 1 token...");
        Thread.Sleep(600);

        if (!limiter.AllowRequest()) {
            Console.WriteLine("Rate limiter failed to refill!");
            return 1;
        }
        Console.WriteLine("Request 7: Allowed (After refill)");
        
        Console.WriteLine("\nC# Token Bucket Rate Limiter Test Passed!");
        return 0;
    }
}