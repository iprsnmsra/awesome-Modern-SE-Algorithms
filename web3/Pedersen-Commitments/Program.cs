using System;

public class Program {
    public class PedersenCommitment {
        private const long p = 2083;
        private const long g = 2;
        private const long h = 3;
        private readonly Random rand = new Random();

        private long ModPow(long baseNum, long exp, long mod) {
            long res = 1;
            long b = baseNum % mod;
            long e = exp;

            while (e > 0) {
                if (e % 2 == 1) res = (res * b) % mod;
                b = (b * b) % mod;
                e /= 2;
            }
            return res;
        }

        public long GenerateBlindingFactor() {
            return rand.Next(1, (int)p - 1);
        }

        public long Commit(long value, long blindingFactor) {
            long cv = ModPow(g, value, p);
            long cr = ModPow(h, blindingFactor, p);
            return (cv * cr) % p;
        }

        public bool Verify(long commitment, long value, long blindingFactor) {
            long expected = Commit(value, blindingFactor);
            return expected == commitment;
        }

        public long HomomorphicAdd(long c1, long c2) {
            return (c1 * c2) % p;
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var crypto = new PedersenCommitment();

        long aliceValue = 5;
        long aliceBlinding = crypto.GenerateBlindingFactor();
        long aliceCommitment = crypto.Commit(aliceValue, aliceBlinding);

        long bobValue = 10;
        long bobBlinding = crypto.GenerateBlindingFactor();
        long bobCommitment = crypto.Commit(bobValue, bobBlinding);

        long networkSumCommitment = crypto.HomomorphicAdd(aliceCommitment, bobCommitment);

        long combinedValue = aliceValue + bobValue;
        long combinedBlinding = aliceBlinding + bobBlinding;

        bool p1 = crypto.Verify(networkSumCommitment, combinedValue, combinedBlinding);
        bool p2 = !crypto.Verify(networkSumCommitment, 999, combinedBlinding);

        if (p1 && p2) {
            Console.WriteLine("C# Pedersen Commitment Test Passed! Homomorphic Confidential Transactions Verified.");
            return 0;
        }
        return 1;
    }
}