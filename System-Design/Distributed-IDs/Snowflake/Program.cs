using System;

public class Program {
    public class SnowflakeGenerator {
        private const long EPOCH = 1609459200000L;
        private const int WORKER_ID_BITS = 5;
        private const int DATACENTER_ID_BITS = 5;
        private const int SEQUENCE_BITS = 12;

        private const long MAX_WORKER_ID = -1L ^ (-1L << WORKER_ID_BITS);
        private const long MAX_DATACENTER_ID = -1L ^ (-1L << DATACENTER_ID_BITS);

        private const int WORKER_SHIFT = SEQUENCE_BITS;
        private const int DATACENTER_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS;
        private const int TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS;

        private const long SEQUENCE_MASK = -1L ^ (-1L << SEQUENCE_BITS);

        private long datacenterId;
        private long workerId;
        private long sequence = 0L;
        private long lastTimestamp = -1L;
        
        private readonly object _lock = new object();

        public SnowflakeGenerator(long datacenterId, long workerId) {
            if (datacenterId > MAX_DATACENTER_ID || datacenterId < 0) {
                throw new ArgumentException("Invalid Datacenter ID");
            }
            if (workerId > MAX_WORKER_ID || workerId < 0) {
                throw new ArgumentException("Invalid Worker ID");
            }
            this.datacenterId = datacenterId;
            this.workerId = workerId;
        }

        private long CurrentTimeMillis() {
            return DateTimeOffset.UtcNow.ToUnixTimeMilliseconds();
        }

        public long NextId() {
            lock (_lock) {
                long timestamp = CurrentTimeMillis();

                if (timestamp < lastTimestamp) {
                    throw new Exception("Clock moved backwards.");
                }

                if (timestamp == lastTimestamp) {
                    sequence = (sequence + 1) & SEQUENCE_MASK;
                    if (sequence == 0) {
                        while (timestamp <= lastTimestamp) {
                            timestamp = CurrentTimeMillis();
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
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var generator = new SnowflakeGenerator(1, 1);
        
        long id1 = generator.NextId();
        long id2 = generator.NextId();
        
        if (id1 != id2 && id2 > id1) {
            Console.WriteLine("C# Snowflake ID Test Passed!");
            Console.WriteLine($"Generated ID 1: {id1}");
            Console.WriteLine($"Generated ID 2: {id2}");
            return 0;
        }
        return 1;
    }
}