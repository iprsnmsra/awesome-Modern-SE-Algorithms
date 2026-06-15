public class Main {
    static class FastMath {
        public static float fastInvSqrt(float number) {
            float threehalfs = 1.5F;
            float x2 = number * 0.5F;
            float y = number;
            
            // Evil floating point bit level hacking natively supported by JVM
            int i = Float.floatToRawIntBits(y);
            
            i = 0x5f3759df - (i >> 1);
            
            y = Float.intBitsToFloat(i);
            
            // 1st iteration of Newton's Method
            y = y * (threehalfs - (x2 * y * y));
            
            return y;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        float testVal = 25.0f;
        
        float standardResult = (float) (1.0 / Math.sqrt(testVal));
        float fastResult = FastMath.fastInvSqrt(testVal);
        
        float errorMargin = Math.abs(standardResult - fastResult);
        
        System.out.println("Standard Math: " + standardResult);
        System.out.println("Fast Inv Sqrt: " + fastResult);
        System.out.println("Error Margin:  " + String.format("%.6f", errorMargin));
        
        if (errorMargin < 0.01) {
            System.out.println("\nJava Fast Inverse Square Root Test Passed! (Hardware Hacker Mode Verified)");
        } else {
            System.exit(1);
        }
    }
}