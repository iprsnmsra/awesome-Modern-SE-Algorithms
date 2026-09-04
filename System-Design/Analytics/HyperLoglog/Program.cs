using System;
using System.Text;

public class Program {
    public class HyperLogLog {
        private readonly int b;
        private readonly int m;
        private readonly int[] registers;
        private readonly double alpha;

        public HyperLogLog(int b = 8) {
            this.b = b;
            this.m = 1 << b;
            this.registers = new int[m];

            if (m == 16) alpha = 0.673;
            else if (m == 32) alpha = 0.697;
            else if (m == 64) alpha = 0.709;
            else alpha = 0.7213 / (1 + 1.079 / m);
        }

        private uint Fnv1a32(string data) {
            uint h = 0x811c9dc5;
            byte[] bytes = Encoding.UTF8.GetBytes(data);
            foreach (byte b in bytes) {
                h ^= b;
                h *= 0x01000193;
            }
            return h;
        }

        public void Add(string item) {
            uint h = Fnv1a32(item);
            uint index = h & (uint)(m - 1);
            uint w = h >> b;

            int rank = 1;
            if (w == 0) {
                rank = 32 - b + 1;
            } else {
                while ((w & 1) == 0) {
                    rank++;
                    w >>= 1;
                }
            }

            registers[index] = Math.Max(registers[index], rank);
        }

        public int Estimate() {
            double Z = 0;
            int v = 0;

            foreach (int r in registers) {
                Z += Math.Pow(2.0, -r);
                if (r == 0) v++;
            }

            double E = (alpha * m * m) / Z;

            if (E <= 2.5 * m && v > 0) {
                E = m * Math.Log((double)m / v);
            }

            return (int)E;
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var hll = new HyperLogLog(8);
        int exactCount = 10000;

        for (int i = 0; i < exactCount; i++) {
            hll.Add($"user_id_{i}");
        }

        int estimatedCount = hll.Estimate();
        double errorPercentage = Math.Abs((double)exactCount - estimatedCount) / exactCount * 100.0;

        Console.WriteLine($"Exact True Count: {exactCount}");
        Console.WriteLine($"HLL Estimation:   {estimatedCount}");
        Console.WriteLine($"Margin of Error:  {errorPercentage:F2}%");

        if (errorPercentage < 10.0) {
            Console.WriteLine("\nC# HyperLogLog Test Passed! Big Data O(1) Memory Engine Verified.");
            return 0;
        }
        return 1;
    }
}