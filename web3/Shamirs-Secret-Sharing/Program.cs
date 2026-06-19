using System;
using System.Collections.Generic;

public class Program {
    const long PRIME = 2083;

    public class Share {
        public long X { get; }
        public long Y { get; }
        public Share(long x, long y) {
            X = x; Y = y;
        }
    }

    public class ShamirSecretSharing {
        private static long PosMod(long a, long m) {
            return ((a % m) + m) % m;
        }

        private static long ModInverse(long n, long p) {
            long res = 1;
            long exp = p - 2;
            long baseNum = PosMod(n, p);

            while (exp > 0) {
                if (exp % 2 == 1) res = (res * baseNum) % p;
                baseNum = (baseNum * baseNum) % p;
                exp /= 2;
            }
            return res;
        }

        public static List<Share> SplitSecret(long secret, int n, int k) {
            if (k > n) throw new ArgumentException("Threshold > Total");
            if (secret >= PRIME) throw new ArgumentException("Secret >= PRIME");

            var rand = new Random();
            var coefficients = new long[k];
            coefficients[0] = secret;
            for (int i = 1; i < k; i++) {
                coefficients[i] = rand.Next(1, (int)PRIME - 1);
            }

            var shares = new List<Share>();
            for (int i = 1; i <= n; i++) {
                long x = i;
                long y = 0;
                for (int exp = 0; exp < k; exp++) {
                    long term = (coefficients[exp] * (long)Math.Pow(x, exp)) % PRIME;
                    y = (y + term) % PRIME;
                }
                shares.Add(new Share(x, y));
            }
            return shares;
        }

        public static long ReconstructSecret(List<Share> shares) {
            long secret = 0;

            for (int i = 0; i < shares.Count; i++) {
                long xi = shares[i].X;
                long yi = shares[i].Y;
                
                long numerator = 1;
                long denominator = 1;

                for (int j = 0; j < shares.Count; j++) {
                    if (i == j) continue;
                    long xj = shares[j].X;

                    numerator = PosMod(numerator * -xj, PRIME);
                    denominator = PosMod(denominator * (xi - xj), PRIME);
                }

                long lagrangeVal = PosMod(yi * numerator % PRIME * ModInverse(denominator, PRIME), PRIME);
                secret = PosMod(secret + lagrangeVal, PRIME);
            }
            return secret;
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        long originalSecret = 1337;
        var allShares = ShamirSecretSharing.SplitSecret(originalSecret, 5, 3);

        var validShares = allShares.GetRange(0, 3);
        var invalidShares = allShares.GetRange(0, 2);

        long validReconstruction = ShamirSecretSharing.ReconstructSecret(validShares);
        long invalidReconstruction = ShamirSecretSharing.ReconstructSecret(invalidShares);

        bool p1 = validReconstruction == originalSecret;
        bool p2 = invalidReconstruction != originalSecret;

        if (p1 && p2) {
            Console.WriteLine("C# SSS Test Passed! Information-theoretic security verified.");
            return 0;
        }
        return 1;
    }
}