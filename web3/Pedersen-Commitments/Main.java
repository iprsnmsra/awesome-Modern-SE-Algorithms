import java.util.Random;

public class Main {
    static class PedersenCommitment {
        private final long p = 2083;
        private final long g = 2;
        private final long h = 3;
        private final Random rand = new Random();

        private long modPow(long base, long exp, long mod) {
            long res = 1;
            long b = base % mod;
            long e = exp;

            while (e > 0) {
                if (e % 2 == 1) res = (res * b) % mod;
                b = (b * b) % mod;
                e /= 2;
            }
            return res;
        }

        public long generateBlindingFactor() {
            return rand.nextInt((int) p - 1) + 1;
        }

        public long commit(long value, long blindingFactor) {
            long cv = modPow(g, value, p);
            long cr = modPow(h, blindingFactor, p);
            return (cv * cr) % p;
        }

        public boolean verify(long commitment, long value, long blindingFactor) {
            long expected = commit(value, blindingFactor);
            return expected == commitment;
        }

        public long homomorphicAdd(long c1, long c2) {
            return (c1 * c2) % p;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        PedersenCommitment crypto = new PedersenCommitment();

        long aliceValue = 5;
        long aliceBlinding = crypto.generateBlindingFactor();
        long aliceCommitment = crypto.commit(aliceValue, aliceBlinding);

        long bobValue = 10;
        long bobBlinding = crypto.generateBlindingFactor();
        long bobCommitment = crypto.commit(bobValue, bobBlinding);

        long networkSumCommitment = crypto.homomorphicAdd(aliceCommitment, bobCommitment);

        long combinedValue = aliceValue + bobValue;
        long combinedBlinding = aliceBlinding + bobBlinding;

        boolean p1 = crypto.verify(networkSumCommitment, combinedValue, combinedBlinding);
        boolean p2 = !crypto.verify(networkSumCommitment, 999, combinedBlinding);

        if (p1 && p2) {
            System.out.println("Java Pedersen Commitment Test Passed! Homomorphic Confidential Transactions Verified.");
        } else {
            System.exit(1);
        }
    }
}