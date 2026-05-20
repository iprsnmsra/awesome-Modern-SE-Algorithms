import { createHash } from 'crypto';

export class MerkleTree {
    private leaves: string[];
    private tree: string[][] = [];
    private root: string;

    constructor(dataBlocks: string[]) {
        this.leaves = dataBlocks.map(block => this.hash(block));
        this.root = this.buildTree();
    }

    private hash(data: string): string {
        return createHash('sha256').update(data).digest('hex');
    }

    private buildTree(): string {
        if (this.leaves.length === 0) return "";

        let currentLevel = this.leaves;
        this.tree.push(currentLevel);

        while (currentLevel.length > 1) {
            const nextLevel: string[] = [];
            for (let i = 0; i < currentLevel.length; i += 2) {
                const left = currentLevel[i];
                // Duplicate last node if odd
                const right = (i + 1 < currentLevel.length) ? currentLevel[i + 1] : left;
                nextLevel.push(this.hash(left + right));
            }
            this.tree.push(nextLevel);
            currentLevel = nextLevel;
        }

        return currentLevel[0];
    }

    public getRoot(): string {
        return this.root;
    }
}

// --- CI/CD Automated Test ---
const txs = ["Block 1", "Block 2", "Block 3"];
const treeOriginal = new MerkleTree(txs);

const txsHacked = ["Block 1", "Block HACKED", "Block 3"];
const treeHacked = new MerkleTree(txsHacked);

if (treeOriginal.getRoot() !== treeHacked.getRoot()) {
    console.log("TypeScript Merkle Tree Test Passed!");
} else {
    process.exit(1);
}