export class KMPSearch {
    private static computeLPS(pattern: string): number[] {
        const m = pattern.length;
        const lps = new Array(m).fill(0);
        let len = 0;
        let i = 1;

        while (i < m) {
            if (pattern[i] === pattern[len]) {
                len++;
                lps[i] = len;
                i++;
            } else {
                if (len !== 0) {
                    len = lps[len - 1];
                } else {
                    lps[i] = 0;
                    i++;
                }
            }
        }
        return lps;
    }

    public static search(text: string, pattern: string): number[] {
        const n = text.length;
        const m = pattern.length;
        if (m === 0) return [];

        const lps = this.computeLPS(pattern);
        const indices: number[] = [];
        let i = 0;
        let j = 0;

        while (i < n) {
            if (pattern[j] === text[i]) {
                i++;
                j++;
            }

            if (j === m) {
                indices.push(i - j);
                j = lps[j - 1];
            } else if (i < n && pattern[j] !== text[i]) {
                if (j !== 0) {
                    j = lps[j - 1];
                } else {
                    i++;
                }
            }
        }
        return indices;
    }
}

// --- CI/CD Automated Test ---
const dnaSequence = "GACACCCTACACAACCACCACACACCCCCACACAC";
const virusSignature = "ACAC";

const matches = KMPSearch.search(dnaSequence, virusSignature);

if (matches.length === 5 && matches.join(',') === "1,9,20,29,31") {
    console.log("TypeScript KMP Search Test Passed!");
} else {
    process.exit(1);
}