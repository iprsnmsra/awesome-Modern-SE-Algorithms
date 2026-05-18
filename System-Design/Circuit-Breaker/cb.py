import time
from enum import Enum

class State(Enum):
    CLOSED = 1
    OPEN = 2
    HALF_OPEN = 3

class CircuitBreaker:
    def __init__(self, failure_threshold: int, cooldown_sec: float):
        self.state = State.CLOSED
        self.failure_threshold = failure_threshold
        self.cooldown_sec = cooldown_sec
        self.failure_count = 0
        self.next_attempt_time = 0.0

    def execute(self, action_func):
        if self.state == State.OPEN:
            if time.time() < self.next_attempt_time:
                return "FAST_FAIL"
            self.state = State.HALF_OPEN

        try:
            success = action_func()
            if not success:
                raise Exception("Action failed")
            self._reset()
            return "SUCCESS"
        except Exception:
            self._record_failure()
            return "FAIL"

    def _record_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.failure_threshold:
            self.state = State.OPEN
            self.next_attempt_time = time.time() + self.cooldown_sec

    def _reset(self):
        self.failure_count = 0
        self.state = State.CLOSED

if __name__ == '__main__':
    cb = CircuitBreaker(failure_threshold=2, cooldown_sec=0.1)
    
    def fail_action():
        return False
        
    cb.execute(fail_action) 
    cb.execute(fail_action)
    res = cb.execute(fail_action) 
    
    assert res == "FAST_FAIL", "Circuit breaker failed to trip!"
    print("Python Test Passed!")