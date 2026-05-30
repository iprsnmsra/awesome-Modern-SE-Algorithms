export class SchnorrZKP {
    constructor(private p: number, private g: number) {}

    // Fast modular exponentiation
    private modExp(base: number, exp: number): number {
        let res = 1;
        base = base % this.p;
        while (exp > 0) {
            if (exp % 2 === 1) res = (res * base) % this.p;
            exp = Math.floor(exp / 2);
            base = (base * base) % this.p;
        }
        return res;
    }

    public generateKeys(secretX: number): number {
        return this.modExp(this.g, secretX);
    }

    public proveAndVerify(secretX: number, publicY: number): boolean {
        // Step 1: Commitment
        const k = Math.floor(Math.random() * (this.p - 2)) + 1;
        const r = this.modExp(this.g, k);

        // Step 2: Challenge
        const c = Math.floor(Math.random() * (this.p - 2)) + 1;

        // Step 3: Response
        const s = k + c * secretX;

        // Step 4: Verification (g^s mod p == (r * y^c) mod p)
        const leftSide = this.modExp(this.g, s);
        const yC = this.modExp(publicY, c);
        const rightSide = (r * yC) % this.p;

        return leftSide === rightSide;
    }
}

// --- CI/CD Automated Test ---
const p = 23;
const g = 5;
const zkp = new SchnorrZKP(p, g);

const aliceSecret = 7;
const alicePublic = zkp.generateKeys(aliceSecret);

const isVerified = zkp.proveAndVerify(aliceSecret, alicePublic);

if (isVerified) {
    console.log("TypeScript Zero-Knowledge Proof Test Passed!");
} else {
    process.exit(1);
}