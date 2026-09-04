import math

class HyperLogLog:
    def __init__(self, b: int = 8):
        # b = 8 means 2^8 = 256 buckets/registers. 
        # Standard Redis uses b=14 (16,384 registers). We use 8 for a lightweight demo.
        self.b = b
        self.m = 1 << b
        self.registers = [0] * self.m
        
        # Flajolet-Martin Alpha Constant for bias correction
        if self.m == 16:
            self.alpha = 0.673
        elif self.m == 32:
            self.alpha = 0.697
        elif self.m == 64:
            self.alpha = 0.709
        else:
            self.alpha = 0.7213 / (1 + 1.079 / self.m)

    def _fnv1a_32(self, data: str) -> int:
        """A simple, robust, zero-dependency 32-bit hash function."""
        h = 0x811c9dc5
        for char in data.encode('utf-8'):
            h ^= char
            h = (h * 0x01000193) & 0xFFFFFFFF
        return h

    def add(self, item: str):
        # 1. Hash the item
        h = self._fnv1a_32(item)
        
        # 2. Use the first 'b' bits for the bucket index
        index = h & (self.m - 1)
        
        # 3. Use the remaining bits for the "coin flips"
        w = h >> self.b
        
        # 4. Count the trailing zeros (streak length) + 1
        rank = 1
        if w == 0:
            rank = 32 - self.b + 1
        else:
            while (w & 1) == 0:
                rank += 1
                w >>= 1
                
        # 5. Store the maximum streak seen for this bucket
        self.registers[index] = max(self.registers[index], rank)

    def estimate(self) -> int:
        """Calculates the estimated cardinality using Harmonic Mean."""
        Z = sum(2.0 ** -r for r in self.registers)
        E = self.alpha * (self.m ** 2) / Z
        
        # Small range correction (Linear Counting) for datasets < 2.5 * m
        if E <= 2.5 * self.m:
            v = self.registers.count(0)
            if v > 0:
                E = self.m * math.log(self.m / v)
                
        return int(E)

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    hll = HyperLogLog(b=8)  # 256 registers
    
    # We will simulate exactly 10,000 UNIQUE users clicking a button.
    exact_count = 10000
    print(f"Loading {exact_count} unique items into HyperLogLog...")
    
    for i in range(exact_count):
        hll.add(f"user_id_{i}")
        
    estimated_count = hll.estimate()
    
    # Mathematical Error Margin calculation
    error_percentage = abs(exact_count - estimated_count) / exact_count * 100
    
    print(f"Exact True Count: {exact_count}")
    print(f"HLL Estimation:   {estimated_count}")
    print(f"Margin of Error:  {error_percentage:.2f}%")
    
    # Standard HLL with b=8 has an expected error rate of ~6.5%. 
    # We assert it remains bounded within 10% for production validity.
    assert error_percentage < 10.0, "Estimation breached statistical bounds!"
    
    print("\nPython HyperLogLog Test Passed! Big Data O(1) Memory Engine Verified.")