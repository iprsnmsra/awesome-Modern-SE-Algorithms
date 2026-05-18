public class Main {
    enum State { CLOSED, OPEN, HALF_OPEN }

    static class CircuitBreaker {
        private State state = State.CLOSED;
        private int failureCount = 0;
        private final int failureThreshold;
        private final long cooldownMs;
        private long nextAttemptTime = 0;

        public CircuitBreaker(int threshold, long cooldownMs) {
            this.failureThreshold = threshold;
            this.cooldownMs = cooldownMs;
        }

        public String execute(java.util.function.Supplier<Boolean> action) {
            if (state == State.OPEN) {
                if (System.currentTimeMillis() < nextAttemptTime) {
                    return "FAST_FAIL";
                }
                state = State.HALF_OPEN;
            }

            try {
                boolean success = action.get();
                if (!success) throw new RuntimeException("Action failed");
                reset();
                return "SUCCESS";
            } catch (Exception e) {
                recordFailure();
                return "FAIL";
            }
        }

        private void recordFailure() {
            failureCount++;
            if (failureCount >= failureThreshold) {
                state = State.OPEN;
                nextAttemptTime = System.currentTimeMillis() + cooldownMs;
            }
        }

        private void reset() {
            failureCount = 0;
            state = State.CLOSED;
        }
    }
    public static void main(String[] args) {
        CircuitBreaker cb = new CircuitBreaker(2, 100);
        cb.execute(() -> false); 
        cb.execute(() -> false); 
        String res = cb.execute(() -> false); 
        
        if ("FAST_FAIL".equals(res)) {
            System.out.println("Java Test Passed!");
        } else {
            System.exit(1);
        }
    }
}