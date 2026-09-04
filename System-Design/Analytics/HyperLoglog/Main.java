public class Main {
    static class HyperLogLog {
        private final int b;
        private final int m;
        private final int[] registers;
        private final double alpha;

        public HyperLogLog(int b) {
            this.b = b;
            this.m = 1 << b;
            this.registers = new int[m];

            if (m == 16) alpha = 0.673;
            else if (m == 32) alpha = 0.697;
            else if (m == 64) alpha = 0.709;
            else alpha = 0.7213 / (1 + 1.079 / m);
        }

        private int fnv1a32(String data) {
            int h = 0x811c9dc5;
            for (byte b : data.getBytes()) {
                h ^= (b & 0xFF);
                h *= 0x01000193;
            }
            return h;
        }

        public void add(String item) {
            int h = fnv1a32(item);
            int index = h & (m - 1);
            int w = h >>> b;

            int rank = 1;
            if (w == 0) {
                rank = 32 - b + 1;
            } else {
                while ((w & 1) == 0) {
                    rank++;
                    w >>>= 1;
                }
            }
            registers[index] = Math.max(registers[index], rank);
        }

        public int estimate() {
            double Z = 0;
            int v = 0;

            for (int r : registers) {
                Z += Math.pow(2.0, -r);
                if (r == 0) v++;
            }

            double E = (alpha * m * m) / Z;

            if (E <= 2.5 * m && v > 0) {
                E = m * Math.log((double) m / v);
            }

            return (int) E;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        HyperLogLog hll = new HyperLogLog(8);
        int exactCount = 10000;

        for (int i = 0; i < exactCount; i++) {
            hll.add("user_id_" + i);
        }

        int estimatedCount = hll.estimate();
        double errorPercentage = Math.abs((double) exactCount - estimatedCount) / exactCount * 100;

        System.out.println("Exact True Count: " + exactCount);
        System.out.println("HLL Estimation:   " + estimatedCount);
        System.out.printf("Margin of Error:  %.2f%%\n", errorPercentage);

        if (errorPercentage < 10.0) {
            System.out.println("\nJava HyperLogLog Test Passed! Big Data O(1) Memory Engine Verified.");
        } else {
            System.exit(1);
        }
    }
}