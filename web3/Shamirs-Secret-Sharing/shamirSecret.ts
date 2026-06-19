const PRIME = 2083;

export class ShamirSecretSharing {
    private static posMod(a: number, m: number): number {
        return ((a % m) + m) % m;
    }

    private static modInverse(n: number, p: number): number {
        // Fermat's Little Theorem: n^(p-2) mod p
        let res = 1;
        let exp = p - 2;
        let base = this.posMod(n, p);

        while (exp > 0) {
            if (exp % 2 === 1) res = (res * base) % p;
            base = (base * base) % p;
            exp = Math.floor(exp / 2);
        }
        return res;
    }

    public static splitSecret(secret: number, n: number, k: number): [number, number][] {
        if (k > n) throw new Error("Threshold cannot be greater than total shares.");
        if (secret >= PRIME) throw new Error(`Secret must be smaller than ${PRIME}.`);

        const coefficients: number[] = [secret];
        for (let i = 1; i < k; i++) {
            coefficients.push(Math.floor(Math.random() * (PRIME - 1)) + 1);
        }

        const shares: [number, number][] = [];
        for (let i = 1; i <= n; i++) {
            let y = 0;
            for (let exp = 0; exp < coefficients.length; exp++) {
                y = (y + coefficients[exp] * Math.pow(i, exp)) % PRIME;
            }
            shares.push([i, y]);
        }

        return shares;
    }

    public static reconstructSecret(shares: [number, number][]): number {
        let secret = 0;

        for (let i = 0; i < shares.length; i++) {
            const [xi, yi] = shares[i];
            let numerator = 1;
            let denominator = 1;

            for (let j = 0; j < shares.length; j++) {
                if (i === j) continue;
                const [xj, yj] = shares[j];

                numerator = this.posMod(numerator * -xj, PRIME);
                denominator = this.posMod(denominator * (xi - xj), PRIME);
            }

            const lagrangeVal = this.posMod(yi * numerator * this.modInverse(denominator, PRIME), PRIME);
            secret = this.posMod(secret + lagrangeVal, PRIME);
        }

        return secret;
    }
}

// --- CI/CD Automated Test ---
const originalSecret = 1337;
const allShares = ShamirSecretSharing.splitSecret(originalSecret, 5, 3);

const validShares = allShares.slice(0, 3);
const invalidShares = allShares.slice(0, 2);

const validReconstruction = ShamirSecretSharing.reconstructSecret(validShares);
const invalidReconstruction = ShamirSecretSharing.reconstructSecret(invalidShares);

const p1 = validReconstruction === originalSecret;
const p2 = invalidReconstruction !== originalSecret;

if (p1 && p2) {
    console.log(`TypeScript SSS Test Passed! Key reconstructed: ${validReconstruction}`);
} else {
    process.exit(1);
}