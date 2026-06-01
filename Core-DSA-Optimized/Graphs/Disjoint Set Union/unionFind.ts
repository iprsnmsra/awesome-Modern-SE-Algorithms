export class UnionFind {
    private parent: number[];
    private rank: number[];

    constructor(size: number) {
        this.parent = new Array(size);
        this.rank = new Array(size).fill(1);
        for (let i = 0; i < size; i++) {
            this.parent[i] = i;
        }
    }

    public find(x: number): number {
        // Path Compression
        if (this.parent[x] !== x) {
            this.parent[x] = this.find(this.parent[x]);
        }
        return this.parent[x];
    }

    public union(x: number, y: number): boolean {
        const rootX = this.find(x);
        const rootY = this.find(y);

        if (rootX === rootY) return false;

        // Union by Rank
        if (this.rank[rootX] > this.rank[rootY]) {
            this.parent[rootY] = rootX;
        } else if (this.rank[rootX] < this.rank[rootY]) {
            this.parent[rootX] = rootY;
        } else {
            this.parent[rootY] = rootX;
            this.rank[rootX]++;
        }
        return true;
    }

    public connected(x: number, y: number): boolean {
        return this.find(x) === this.find(y);
    }
}

// --- CI/CD Automated Test ---
const uf = new UnionFind(5);

uf.union(0, 1);
uf.union(1, 2);
uf.union(3, 4);

if (uf.connected(0, 2) && !uf.connected(0, 3)) {
    uf.union(2, 4);
    if (uf.connected(0, 3)) {
        console.log("TypeScript Union-Find Test Passed!");
    } else {
        process.exit(1);
    }
} else {
    process.exit(1);
}