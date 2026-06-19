import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Main {
    static final long PRIME = 2083;

    static class Share {
        long x, y;
        public Share(long x, long y) {
            this.x = x; this.y = y;
        }
    }

    static class ShamirSecretSharing {
        private static long posMod(long a, long m) {
            return ((a % m) + m) % m;
        }

        private static long modInverse(long n, long p) {
            long res = 1;
            long exp = p - 2;
            long base = posMod(n, p);

            while (exp > 0) {
                if (exp % 2 == 1) res = (res * base) % p;
                base = (base * base) % p;
                exp /= 2;
            }
            return res;
        }

        public static List<Share> splitSecret(long secret, int n, int k) {
            if (k > n) throw new IllegalArgumentException("Threshold > Total");
            if (secret >= PRIME) throw new IllegalArgumentException("Secret >= PRIME");

            Random rand = new Random();
            long[] coefficients = new long[k];
            coefficients[0] = secret;
            for (int i = 1; i < k; i++) {
                coefficients[i] = rand.nextInt((int) PRIME - 1) + 1;
            }

            List<Share> shares = new ArrayList<>();
            for (int i = 1; i <= n; i++) {
                long x = i;
                long y = 0;
                for (int exp = 0; exp < k; exp++) {
                    long term = (coefficients[exp] * (long) Math.pow(x, exp)) % PRIME;
                    y = (y + term) % PRIME;
                }
                shares.add(new Share(x, y));
            }
            return shares;
        }

        public static long reconstructSecret(List<Share> shares) {
            long secret = 0;

            for (int i = 0; i < shares.size(); i++) {
                long xi = shares.get(i).x;
                long yi = shares.get(i).y;
                
                long numerator = 1;
                long denominator = 1;

                for (int j = 0; j < shares.size(); j++) {
                    if (i == j) continue;
                    long xj = shares.get(j).x;

                    numerator = posMod(numerator * -xj, PRIME);
                    denominator = posMod(denominator * (xi - xj), PRIME);
                }

                long lagrangeVal = posMod(yi * numerator % PRIME * modInverse(denominator, PRIME), PRIME);
                secret = posMod(secret + lagrangeVal, PRIME);
            }
            return secret;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        long originalSecret = 1337;
        List<Share> allShares = ShamirSecretSharing.splitSecret(originalSecret, 5, 3);

        List<Share> validShares = allShares.subList(0, 3);
        List<Share> invalidShares = allShares.subList(0, 2);

        long validReconstruction = ShamirSecretSharing.reconstructSecret(validShares);
        long invalidReconstruction = ShamirSecretSharing.reconstructSecret(invalidShares);

        boolean p1 = validReconstruction == originalSecret;
        boolean p2 = invalidReconstruction != originalSecret;

        if (p1 && p2) {
            System.out.println("Java SSS Test Passed! Information-theoretic security verified.");
        } else {
            System.exit(1);
        }
    }
}