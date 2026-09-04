export class HyperLogLog {
    private b: number;
    private m: number;
    private registers: number[];
    private alpha: number;

    constructor(b: number = 8) {
        this.b = b;
        this.m = 1 << b;
        this.registers = new Array(this.m).fill(0);

        if (this.m === 16) this.alpha = 0.673;
        else if (this.m === 32) this.alpha = 0.697;
        else if (this.m === 64) this.alpha = 0.709;
        else this.alpha = 0.7213 / (1 + 1.079 / this.m);
    }

    private fnv1a32(data: string): number {
        let h = 0x811c9dc5;
        for (let i = 0; i < data.length; i++) {
            h ^= data.charCodeAt(i);
            h = Math.imul(h, 0x01000193);
        }
        return h >>> 0; // Force unsigned 32-bit
    }

    public add(item: string): void {
        const h = this.fnv1a32(item);
        const index = h & (this.m - 1);
        let w = h >>> this.b;

        let rank = 1;
        if (w === 0) {
            rank = 32 - this.b + 1;
        } else {
            while ((w & 1) === 0) {
                rank++;
                w >>>= 1;
            }
        }

        this.registers[index] = Math.max(this.registers[index], rank);
    }

    public estimate(): number {
        let Z = 0;
        let v = 0; // Count of empty registers

        for (let i = 0; i < this.m; i++) {
            Z += Math.pow(2.0, -this.registers[i]);
            if (this.registers[i] === 0) v++;
        }

        let E = (this.alpha * this.m * this.m) / Z;

        // Linear Counting correction for small ranges
        if (E <= 2.5 * this.m) {
            if (v > 0) {
                E = this.m * Math.log(this.m / v);
            }
        }

        return Math.floor(E);
    }
}

// --- CI/CD Automated Test ---
const hll = new HyperLogLog(8);
const exactCount = 10000;

for (let i = 0; i < exactCount; i++) {
    hll.add(`user_id_${i}`);
}

const estimatedCount = hll.estimate();
const errorPercentage = Math.abs(exactCount - estimatedCount) / exactCount * 100;

console.log(`Exact True Count: ${exactCount}`);
console.log(`HLL Estimation:   ${estimatedCount}`);
console.log(`Margin of Error:  ${errorPercentage.toFixed(2)}%`);

if (errorPercentage < 10.0) {
    console.log("TypeScript HyperLogLog Test Passed! Big Data O(1) Memory Engine Verified.");
} else {
    process.exit(1);
}