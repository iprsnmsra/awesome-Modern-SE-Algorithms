import time
import threading

class TokenBucket:
    def __init__(self, capacity: int, refill_rate_per_second: float):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_second
        self.tokens = capacity
        self.last_refill_timestamp = time.time()
        self.lock = threading.Lock()

    def _refill(self):
        now = time.time()
        time_passed = now - self.last_refill_timestamp
        
        # Calculate how many tokens to add based on time passed
        tokens_to_add = time_passed * self.refill_rate
        
        if tokens_to_add > 0:
            # Add tokens, but cap it at maximum capacity
            self.tokens = min(self.capacity, self.tokens + tokens_to_add)
            self.last_refill_timestamp = now

    def allow_request(self) -> bool:
        with self.lock:
            self._refill()
            
            if self.tokens >= 1.0:
                self.tokens -= 1.0
                return True
            return False

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    # Bucket holds max 5 tokens, refills 2 tokens every 1 second (0.5s per token)
    limiter = TokenBucket(capacity=5, refill_rate_per_second=2.0)
    
    print("Simulating a burst of 6 rapid requests...")
    
    # 1. First 5 requests should pass instantly (Burst tolerance)
    for i in range(5):
        assert limiter.allow_request() == True, f"Request {i+1} was falsely blocked!"
        print(f"Request {i+1}: Allowed")
        
    # 2. The 6th request should be blocked (Bucket is empty)
    assert limiter.allow_request() == False, "Rate limiter failed to block excess traffic!"
    print("Request 6: Blocked (HTTP 429 Too Many Requests)")
    
    # 3. Wait for exactly 1 token to refill (0.5 seconds)
    print("Waiting 0.6 seconds for bucket to refill 1 token...")
    time.sleep(0.6)
    
    # 4. Request should now pass
    assert limiter.allow_request() == True, "Rate limiter failed to refill!"
    print("Request 7: Allowed (After refill)")
    
    print("\nPython Token Bucket Rate Limiter Test Passed!")