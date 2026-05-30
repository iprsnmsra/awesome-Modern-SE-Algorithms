using System;

public class Program {
    class SchnorrZKP {
        private int p;
        private int g;
        private Random rand = new Random();

        public SchnorrZKP(int p, int g) {
            this.p = p;
            this.g = g;
        }

        private int ModExp(int baseNum, int exp) {
            int res = 1;
            baseNum = baseNum % p;
            while (exp > 0) {
                if (exp % 2 == 1) res = (res * baseNum) % p;
                exp >>= 1;
                baseNum = (baseNum * baseNum) % p;
            }
            return res;
        }

        public int GenerateKeys(int secretX) {
            return ModExp(g, secretX);
        }

        public bool ProveAndVerify(int secretX, int publicY) {
            // Step 1: Commitment
            int k = rand.Next(1, p - 1);
            int r = ModExp(g, k);

            // Step 2: Challenge
            int c = rand.Next(1, p - 1);

            // Step 3: Response
            int s = k + c * secretX;

            // Step 4: Verification
            int leftSide = ModExp(g, s);
            int yC = ModExp(publicY, c);
            int rightSide = (r * yC) % p;

            return leftSide == rightSide;
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        int p = 23;
        int g = 5;
        var zkp = new SchnorrZKP(p, g);

        int aliceSecret = 7;
        int alicePublic = zkp.GenerateKeys(aliceSecret);

        bool isVerified = zkp.ProveAndVerify(aliceSecret, alicePublic);

        if (isVerified) {
            Console.WriteLine("C# Zero-Knowledge Proof Test Passed!");
            return 0;
        }
        return 1;
    }
}