export class TarjanSCC {
    private id = 0;
    private ids: Int32Array;
    private low: Int32Array;
    private onStack: Uint8Array;
    private stack: number[] = [];
    private sccs: number[][] = [];
    private graph: number[][];

    constructor(n: number, graph: number[][]) {
        this.ids = new Int32Array(n).fill(-1);
        this.low = new Int32Array(n);
        this.onStack = new Uint8Array(n);
        this.graph = graph;
    }

    private dfs(at: number): void {
        this.stack.push(at);
        this.onStack[at] = 1;
        this.ids[at] = this.low[at] = this.id++;

        for (const to of this.graph[at]) {
            if (this.ids[to] === -1) this.dfs(to);
            if (this.onStack[to] === 1) this.low[at] = Math.min(this.low[at], this.low[to]);
        }

        if (this.ids[at] === this.low[at]) {
            const scc: number[] = [];
            let node = -1;
            while (node !== at) {
                node = this.stack.pop()!;
                this.onStack[node] = 0;
                scc.push(node);
            }
            this.sccs.push(scc);
        }
    }

    public findSCCs(): number[][] {
        for (let i = 0; i < this.ids.length; i++) {
            if (this.ids[i] === -1) this.dfs(i);
        }
        return this.sccs;
    }
}

// --- CI/CD Automated Test ---
const graph = [[1], [2], [0], [4], []];
const tarjan = new TarjanSCC(5, graph);
const result = tarjan.findSCCs();

if (result.length === 3) {
    console.log("TypeScript Tarjan SCC Test Passed!");
} else {
    process.exit(1);
}