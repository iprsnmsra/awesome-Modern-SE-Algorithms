using System;

public class Program {
    public class FastMath {
        public static float FastInvSqrt(float number) {
            float threehalfs = 1.5f;
            float x2 = number * 0.5f;
            float y = number;
            
            // Direct bit-casting supported by .NET Core
            int i = BitConverter.SingleToInt32Bits(y);
            
            i = 0x5f3759df - (i >> 1);
            
            y = BitConverter.Int32BitsToSingle(i);
            
            // 1st iteration of Newton's Method
            y = y * (threehalfs - (x2 * y * y));
            
            return y;
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        float testVal = 25.0f;
        
        float standardResult = (float)(1.0 / Math.Sqrt(testVal));
        float fastResult = FastMath.FastInvSqrt(testVal);
        
        float errorMargin = Math.Abs(standardResult - fastResult);
        
        Console.WriteLine($"Standard Math: {standardResult}");
        Console.WriteLine($"Fast Inv Sqrt: {fastResult}");
        Console.WriteLine($"Error Margin:  {errorMargin:F6}");
        
        if (errorMargin < 0.01) {
            Console.WriteLine("\nC# Fast Inverse Square Root Test Passed! (Hardware Hacker Mode Verified)");
            return 0;
        }
        return 1;
    }
}