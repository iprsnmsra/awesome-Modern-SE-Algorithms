export class BPETokenizer {
    private numMerges: number;
    private merges: Map<string, string> = new Map();

    constructor(numMerges: number) {
        this.numMerges = numMerges;
    }

    public train(text: string): void {
        const words = text.split(/\s+/);
        let wordCounts: Map<string[], number> = new Map();

        for (const word of words) {
            if (word.length === 0) continue;
            const split = [...word, "</w>"];
            
            // Check for existing matching array references
            let found = false;
            for (const [key, val] of wordCounts.entries()) {
                if (key.join(",") === split.join(",")) {
                    wordCounts.set(key, val + 1);
                    found = true;
                    break;
                }
            }
            if (!found) wordCounts.set(split, 1);
        }

        for (let i = 0; i < this.numMerges; i++) {
            const pairs: Map<string, number> = new Map();

            for (const [wordTuple, freq] of wordCounts.entries()) {
                for (let j = 0; j < wordTuple.length - 1; j++) {
                    const pairStr = `${wordTuple[j]},${wordTuple[j + 1]}`;
                    pairs.set(pairStr, (pairs.get(pairStr) || 0) + freq);
                }
            }

            if (pairs.size === 0) break;

            // Extract best pair
            let bestPairStr = "";
            let maxFreq = -1;
            for (const [pair, freq] of pairs.entries()) {
                if (freq > maxFreq) {
                    maxFreq = freq;
                    bestPairStr = pair;
                }
            }

            if (maxFreq < 1) break;

            const bestPair = bestPairStr.split(",");
            const newToken = bestPair.join("");
            this.merges.set(bestPairStr, newToken);

            const newWordCounts: Map<string[], number> = new Map();
            for (const [wordTuple, freq] of wordCounts.entries()) {
                const newWord: string[] = [];
                let j = 0;
                while (j < wordTuple.length) {
                    if (j < wordTuple.length - 1 && wordTuple[j] === bestPair[0] && wordTuple[j + 1] === bestPair[1]) {
                        newWord.push(newToken);
                        j += 2;
                    } else {
                        newWord.push(wordTuple[j]);
                        j++;
                    }
                }
                newWordCounts.set(newWord, freq);
            }
            wordCounts = newWordCounts;
        }
    }

    public tokenize(text: string): string[] {
        const words = text.split(/\s+/);
        const outputTokens: string[] = [];

        for (const word of words) {
            if (word.length === 0) continue;
            let tokens = [...word, "</w>"];

            while (tokens.length > 1) {
                let pairToMerge: string[] | null = null;
                
                // Scan tokens to see which of our rules applies first
                for (let i = 0; i < tokens.length - 1; i++) {
                    const checkKey = `${tokens[i]},${tokens[i + 1]}`;
                    if (this.merges.has(checkKey)) {
                        pairToMerge = [tokens[i], tokens[i + 1]];
                        break;
                    }
                }

                if (!pairToMerge) break;

                const matchKey = `${pairToMerge[0]},${pairToMerge[1]}`;
                const targetToken = this.merges.get(matchKey)!;
                const newTokens: string[] = [];
                let i = 0;
                while (i < tokens.length) {
                    if (i < tokens.length - 1 && tokens[i] === pairToMerge[0] && tokens[i + 1] === pairToMerge[1]) {
                        newTokens.push(targetToken);
                        i += 2;
                    } else {
                        newTokens.push(tokens[i]);
                        i++;
                    }
                }
                tokens = newTokens;
            }
            outputTokens.push(...tokens);
        }
        return outputTokens;
    }
}

// --- CI/CD Automated Test ---
const tokenizer = new BPETokenizer(10);
tokenizer.train("hug pug hug pug hug pug shug");
const result = tokenizer.tokenize("hug pug");

if (result.length < 8 && result.length > 0) {
    console.log("TypeScript BPE Tokenizer Test Passed!");
} else {
    process.exit(1);
}