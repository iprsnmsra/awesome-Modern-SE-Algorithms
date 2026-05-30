import java.util.Random;

public class Main {
    static class SchnorrZKP {
        private int p;
        private int g;
        private Random rand = new Random();

        public SchnorrZKP(int p, int g) {
            this.p = p;
            this.g = g;
        }

        private int modExp(int base, int exp) {
            int res = 1;
            base = base % p;
            while (exp > 0) {
                if (exp % 2 == 1) res = (res * base) % p;
                exp = exp >> 1;
                base = (base * base) % p;
            }
            return res;
        }

        public int generateKeys(int secretX) {
            return modExp(g, secretX);
        }

        public boolean proveAndVerify(int secretX, int publicY) {
            // Step 1: Commitment
            int k = rand.nextInt(p - 2) + 1;
            int r = modExp(g, k);

            // Step 2: Challenge
            int c = rand.nextInt(p - 2) + 1;

            // Step 3: Response
            int s = k + c * secretX;

            // Step 4: Verification
            int leftSide = modExp(g, s);
            int yC = modExp(publicY, c);
            int rightSide = (r * yC) % p;

            return leftSide == rightSide;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        int p = 23;
        int g = 5;
        SchnorrZKP zkp = new SchnorrZKP(p, g);

        int aliceSecret = 7;
        int alicePublic = zkp.generateKeys(aliceSecret);

        boolean isVerified = zkp.proveAndVerify(aliceSecret, alicePublic);

        if (isVerified) {
            System.out.println("Java Zero-Knowledge Proof Test Passed!");
        } else {
            System.exit(1);
        }
    }
}