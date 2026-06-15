import struct
import math
import time

class FastMath:
    @staticmethod
    def fast_inv_sqrt(number: float) -> float:
        """
        Python implementation of the Quake III Fast Inverse Square Root.
        Because Python abstracts memory, we use the `struct` module to pack 
        and unpack the binary bits directly.
        """
        if number <= 0:
            raise ValueError("Input must be a positive number.")
            
        threehalfs = 1.5
        x2 = number * 0.5
        y = number
        
        packed_y = struct.pack('f', y)
        i = struct.unpack('i', packed_y)[0]
        i = 0x5f3759df - (i >> 1)

        packed_i = struct.pack('i', i)
        y = struct.unpack('f', packed_i)[0]

        y = y * (threehalfs - (x2 * y * y))
        
        return y

if __name__ == '__main__':
    test_val = 25.0
    
    # 1 / sqrt(25) should be exactly 0.2
    standard_result = 1.0 / math.sqrt(test_val)
    fast_result = FastMath.fast_inv_sqrt(test_val)
    
    error_margin = abs(standard_result - fast_result)
    
    print(f"Standard Math: {standard_result}")
    print(f"Fast Inv Sqrt: {fast_result}")
    print(f"Error Margin:  {error_margin:.6f}")
    
    assert error_margin < 0.01, "Approximation failed! Error margin too high."
    
    print("\nPython Fast Inverse Square Root Test Passed! (Hardware Hacker Mode Verified)")