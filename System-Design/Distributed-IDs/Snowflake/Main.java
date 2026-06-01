public class Main {
    static class SnowflakeGenerator {
        private final long EPOCH = 1609459200000L;
        private final long WORKER_ID_BITS = 5L;
        private final long DATACENTER_ID_BITS = 5L;
        private final long SEQUENCE_BITS = 12L;

        private final long MAX_WORKER_ID = ~(-1L << WORKER_ID_BITS);
        private final long MAX_DATACENTER_ID = ~(-1L << DATACENTER_ID_BITS);

        private final long WORKER_SHIFT = SEQUENCE_BITS;
        private final long DATACENTER_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS;
        private final long TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS;

        private final long SEQUENCE_MASK = ~(-1L << SEQUENCE_BITS);

        private long datacenterId;
        private long workerId;
        private long sequence = 0L;
        private long lastTimestamp = -1L;

        public SnowflakeGenerator(long datacenterId, long workerId) {
            if (datacenterId > MAX_DATACENTER_ID || datacenterId < 0) {
                throw new IllegalArgumentException("Invalid Datacenter ID");
            }
            if (workerId > MAX_WORKER_ID || workerId < 0) {
                throw new IllegalArgumentException("Invalid Worker ID");
            }
            this.datacenterId = datacenterId;
            this.workerId = workerId;
        }

        private long currentTimeMillis() {
            return System.currentTimeMillis();
        }

        public synchronized long nextId() {
            long timestamp = currentTimeMillis();

            if (timestamp < lastTimestamp) {
                throw new RuntimeException("Clock moved backwards.");
            }

            if (timestamp == lastTimestamp) {
                sequence = (sequence + 1) & SEQUENCE_MASK;
                if (sequence == 0) {
                    while (timestamp <= lastTimestamp) {
                        timestamp = currentTimeMillis();
                    }
                }
            } else {
                sequence = 0L;
            }

            lastTimestamp = timestamp;

            return ((timestamp - EPOCH) << TIMESTAMP_SHIFT) |
                   (datacenterId << DATACENTER_SHIFT) |
                   (workerId << WORKER_SHIFT) |
                   sequence;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        SnowflakeGenerator generator = new SnowflakeGenerator(1, 1);
        
        long id1 = generator.nextId();
        long id2 = generator.nextId();
        
        if (id1 != id2 && id2 > id1) {
            System.out.println("Java Snowflake ID Test Passed!");
            System.out.println("Generated ID 1: " + id1);
            System.out.println("Generated ID 2: " + id2);
        } else {
            System.exit(1);
        }
    }
}