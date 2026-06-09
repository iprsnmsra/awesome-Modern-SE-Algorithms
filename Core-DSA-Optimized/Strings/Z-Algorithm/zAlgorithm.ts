export class ZAlgorithm {
    private static getZArray(s: string): number[] {
        const n = s.length;
        const z = new Array(n).fill(0);
        let L = 0, R = 0;

        for (let i = 1; i < n; i++) {
            if (i <= R) {
                z[i] = Math.min(R - i + 1, z[i - L]);
            }

            while (i + z[i] < n && s[z[i]] === s[i + z[i]]) {
                z[i]++;
            }

            if (i + z[i] - 1 > R) {
                L = i;
                R = i + z[i] - 1;
            }
        }

        return z;
    }

    public static search(pattern: string, text: string): number[] {
        const matches: number[] = [];
        if (pattern.length === 0 || text.length === 0) return matches;

        const concat = pattern + "$" + text;
        const m = pattern.length;
        const zArray = this.getZArray(concat);

        for (let i = 0; i < zArray.length; i++) {
            if (zArray[i] === m) {
                matches.push(i - m - 1);
            }
        }

        return matches;
    }
}

// --- CI/CD Automated Test ---
const text = "AABAACAADAABAABA";
const pattern = "AABA";

const results = ZAlgorithm.search(pattern, text);

if (results.length === 3 && results[0] === 0 && results[1] === 9 && results[2] === 12) {
    console.log("TypeScript Z-Algorithm Pattern Matching Test Passed!");
} else {
    process.exit(1);
}