#include <iostream>
#include <chrono>
#include <thread>
#include <mutex>
#include <algorithm>
#include <cassert>

using namespace std;

class TokenBucket {
private:
    double capacity;
    double refillRatePerSecond;
    double tokens;
    chrono::steady_clock::time_point lastRefillTimestamp;
    mutex mtx;

    void refill() {
        auto now = chrono::steady_clock::now();
        chrono::duration<double> timePassed = now - lastRefillTimestamp;
        
        double tokensToAdd = timePassed.count() * refillRatePerSecond;
        
        if (tokensToAdd > 0) {
            tokens = min(capacity, tokens + tokensToAdd);
            lastRefillTimestamp = now;
        }
    }

public:
    TokenBucket(double cap, double refillRate) : capacity(cap), refillRatePerSecond(refillRate), tokens(cap) {
        lastRefillTimestamp = chrono::steady_clock::now();
    }

    bool allowRequest() {
        lock_guard<mutex> lock(mtx);
        refill();
        
        if (tokens >= 1.0) {
            tokens -= 1.0;
            return true;
        }
        return false;
    }
};

// --- CI/CD Automated Test ---
int main() {
    TokenBucket limiter(5.0, 2.0);
    cout << "Simulating a burst of 6 rapid requests...\n";

    for (int i = 0; i < 5; i++) {
        assert(limiter.allowRequest() == true);
        cout << "Request " << (i + 1) << ": Allowed\n";
    }

    assert(limiter.allowRequest() == false);
    cout << "Request 6: Blocked (HTTP 429)\n";

    cout << "Waiting 0.6 seconds for bucket to refill 1 token...\n";
    this_thread::sleep_for(chrono::milliseconds(600));

    assert(limiter.allowRequest() == true);
    cout << "Request 7: Allowed (After refill)\n";
    
    cout << "\nC++ Token Bucket Rate Limiter Test Passed!\n";
    return 0;
}