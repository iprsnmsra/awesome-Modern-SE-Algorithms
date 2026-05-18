#include <iostream>
#include <functional>
#include <chrono>

enum class State { CLOSED, OPEN, HALF_OPEN };

class CircuitBreaker {
private:
    State state = State::CLOSED;
    int failureCount = 0;
    int failureThreshold;
    long long cooldownMs;
    long long nextAttemptTime = 0;

    long long now() {
        return std::chrono::duration_cast<std::chrono::milliseconds>(
            std::chrono::system_clock::now().time_since_epoch()
        ).count();
    }

    void recordFailure() {
        failureCount++;
        if (failureCount >= failureThreshold) {
            state = State::OPEN;
            nextAttemptTime = now() + cooldownMs;
        }
    }

    void reset() {
        failureCount = 0;
        state = State::CLOSED;
    }

public:
    CircuitBreaker(int threshold, long long cooldown) 
        : failureThreshold(threshold), cooldownMs(cooldown) {}

    std::string execute(std::function<bool()> action) {
        if (state == State::OPEN) {
            if (now() < nextAttemptTime) return "FAST_FAIL";
            state = State::HALF_OPEN;
        }

        try {
            if (!action()) throw std::runtime_error("Failed");
            reset();
            return "SUCCESS";
        } catch (...) {
            recordFailure();
            return "FAIL";
        }
    }
};
int main() {
    CircuitBreaker cb(2, 100);
    auto alwaysFail = []() { return false; };
    
    cb.execute(alwaysFail);
    cb.execute(alwaysFail); 
    std::string res = cb.execute(alwaysFail); 
    
    if (res == "FAST_FAIL") {
        std::cout << "C++ Test Passed!\n";
        return 0;
    }
    return 1;
}