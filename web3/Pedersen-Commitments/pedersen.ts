const P = 2083n;
const G = 2n;
const H = 3n;

export class PedersenCommitment {
    private static modPow(base: bigint, exp: bigint, mod: bigint): bigint {
        let res = 1n;
        let b = base % mod;
        let e = exp;

        while (e > 0n) {
            if (e % 2n === 1n) res = (res * b) % mod;
            b = (b * b) % mod;
            e = e / 2n;
        }
        return res;
    }

    public static generateBlindingFactor(): bigint {
        return BigInt(Math.floor(Math.random() * (Number(P) - 1)) + 1);
    }

    public static commit(value: bigint, blindingFactor: bigint): bigint {
        const cv = this.modPow(G, value, P);
        const cr = this.modPow(H, blindingFactor, P);
        return (cv * cr) % P;
    }

    public static verify(commitment: bigint, value: bigint, blindingFactor: bigint): boolean {
        const expected = this.commit(value, blindingFactor);
        return expected === commitment;
    }

    public static homomorphicAdd(c1: bigint, c2: bigint): bigint {
        return (c1 * c2) % P;
    }
}

// --- CI/CD Automated Test ---
const aliceValue = 5n;
const aliceBlinding = PedersenCommitment.generateBlindingFactor();
const aliceCommitment = PedersenCommitment.commit(aliceValue, aliceBlinding);

const bobValue = 10n;
const bobBlinding = PedersenCommitment.generateBlindingFactor();
const bobCommitment = PedersenCommitment.commit(bobValue, bobBlinding);

const networkSumCommitment = PedersenCommitment.homomorphicAdd(aliceCommitment, bobCommitment);

const combinedValue = aliceValue + bobValue;
const combinedBlinding = aliceBlinding + bobBlinding;

const p1 = PedersenCommitment.verify(networkSumCommitment, combinedValue, combinedBlinding);
const p2 = !PedersenCommitment.verify(networkSumCommitment, 999n, combinedBlinding);

if (p1 && p2) {
    console.log("TypeScript Pedersen Commitment Test Passed! Homomorphic Confidential Transactions Verified.");
} else {
    process.exit(1);
}