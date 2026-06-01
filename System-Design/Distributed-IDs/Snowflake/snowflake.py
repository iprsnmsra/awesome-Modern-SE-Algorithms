import time

class SnowflakeGenerator:
    # Custom Epoch (Jan 1, 2021) to maximize the 69-year lifespan
    EPOCH = 1609459200000

    # Bit distribution
    WORKER_ID_BITS = 5
    DATACENTER_ID_BITS = 5
    SEQUENCE_BITS = 12

    MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)
    MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)

    # Left shift amounts
    WORKER_SHIFT = SEQUENCE_BITS
    DATACENTER_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
    TIMESTAMP_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

    SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

    def __init__(self, datacenter_id: int, worker_id: int):
        if datacenter_id > self.MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError(f"Datacenter ID must be between 0 and {self.MAX_DATACENTER_ID}")
        if worker_id > self.MAX_WORKER_ID or worker_id < 0:
            raise ValueError(f"Worker ID must be between 0 and {self.MAX_WORKER_ID}")
            
        self.datacenter_id = datacenter_id
        self.worker_id = worker_id
        self.sequence = 0
        self.last_timestamp = -1

    def _current_time_millis(self) -> int:
        return int(time.time() * 1000)

    def next_id(self) -> int:
        timestamp = self._current_time_millis()

        # Handle NTP Clock Drift
        if timestamp < self.last_timestamp:
            raise Exception("Clock moved backwards. Refusing to generate id.")

        if timestamp == self.last_timestamp:
            # Same millisecond, increment the sequence
            self.sequence = (self.sequence + 1) & self.SEQUENCE_MASK
            if self.sequence == 0:
                # Sequence exhausted (4096 IDs generated in 1ms). Wait for next ms.
                while timestamp <= self.last_timestamp:
                    timestamp = self._current_time_millis()
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        # Bitwise assembly of the 64-bit integer
        return ((timestamp - self.EPOCH) << self.TIMESTAMP_SHIFT) | \
               (self.datacenter_id << self.DATACENTER_SHIFT) | \
               (self.worker_id << self.WORKER_SHIFT) | \
               self.sequence

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    generator = SnowflakeGenerator(datacenter_id=1, worker_id=1)
    
    id1 = generator.next_id()
    id2 = generator.next_id()
    
    # 1. Verify uniqueness
    assert id1 != id2, "Generated duplicate IDs!"
    
    # 2. Verify chronological sorting (K-Sortable)
    assert id2 > id1, "IDs are not sorting chronologically!"
    
    print(f"Python Snowflake ID Test Passed!")
    print(f"Generated ID 1: {id1}")
    print(f"Generated ID 2: {id2}")