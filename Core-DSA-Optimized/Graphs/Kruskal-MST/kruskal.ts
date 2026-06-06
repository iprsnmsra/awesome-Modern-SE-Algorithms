class UnionFind {
    private parent: number[];
    private rank: number[];

    constructor(size: number) {
        this.parent = Array.from({ length: size }, (_, i) => i);
        this.rank = new Array(size).fill(1);
    }

    public find(x: number): number {
        if (this.parent[x] !== x) {
            this.parent[x] = this.find(this.parent[x]); // Path Compression
        }
        return this.parent[x];
    }

    public union(x: number, y: number): boolean {
        const rootX = this.find(x);
        const rootY = this.find(y);

        if (rootX === rootY) return false;

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
}

class Edge {
    constructor(public u: number, public v: number, public weight: number) {}
}

export class KruskalMST {
    private V: number;
    private edges: Edge[];

    constructor(vertices: number) {
        this.V = vertices;
        this.edges = [];
    }

    public addEdge(u: number, v: number, weight: number): void {
        this.edges.push(new Edge(u, v, weight));
    }

    public solve(): { mst: Edge[], minCost: number } {
        // 1. Sort edges
        this.edges.sort((a, b) => a.weight - b.weight);

        const uf = new UnionFind(this.V);
        const mst: Edge[] = [];
        let minCost = 0;

        // 2. Iterate
        for (const edge of this.edges) {
            // 3. Union-Find cycle check
            if (uf.union(edge.u, edge.v)) {
                mst.push(edge);
                minCost += edge.weight;

                if (mst.length === this.V - 1) break;
            }
        }

        if (mst.length !== this.V - 1) {
            throw new Error("Graph is disconnected!");
        }

        return { mst, minCost };
    }
}

// --- CI/CD Automated Test ---
const kruskal = new KruskalMST(4);
kruskal.addEdge(0, 1, 10);
kruskal.addEdge(0, 2, 6);
kruskal.addEdge(0, 3, 5);
kruskal.addEdge(1, 3, 15);
kruskal.addEdge(2, 3, 4);

const result = kruskal.solve();

if (result.minCost === 19 && result.mst.length === 3) {
    console.log(`TypeScript Kruskal's Algorithm Test Passed! Minimum Network Cost: ${result.minCost}`);
} else {
    process.exit(1);
}