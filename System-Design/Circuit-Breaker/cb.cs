using System;

public class Program {
    enum State { CLOSED, OPEN, HALF_OPEN }

    class CircuitBreaker {
        private State state = State.CLOSED;
        private int failureCount = 0;
        private readonly int failureThreshold;
        private readonly long cooldownTicks;
        private long nextAttemptTicks = 0;

        public CircuitBreaker(int threshold, int cooldownMs) {
            failureThreshold = threshold;
            cooldownTicks = cooldownMs * TimeSpan.TicksPerMillisecond;
        }

        public string Execute(Func<bool> action) {
            if (state == State.OPEN) {
                if (DateTime.UtcNow.Ticks < nextAttemptTicks) {
                    return "FAST_FAIL";
                }
                state = State.HALF_OPEN;
            }

            try {
                if (!action()) throw new Exception("Action failed");
                Reset();
                return "SUCCESS";
            } catch {
                RecordFailure();
                return "FAIL";
            }
        }

        private void RecordFailure() {
            failureCount++;
            if (failureCount >= failureThreshold) {
                state = State.OPEN;
                nextAttemptTicks = DateTime.UtcNow.Ticks + cooldownTicks;
            }
        }

        private void Reset() {
            failureCount = 0;
            state = State.CLOSED;
        }
    }
    public static int Main() {
        var cb = new CircuitBreaker(2, 100);
        Func<bool> alwaysFail = () => false;
        
        cb.Execute(alwaysFail);
        cb.Execute(alwaysFail); 
        string res = cb.Execute(alwaysFail); 
        
        if (res == "FAST_FAIL") {
            Console.WriteLine("C# Test Passed!");
            return 0;
        }
        return 1;
    }
}