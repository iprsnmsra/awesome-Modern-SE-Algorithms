export class FloydWarshall {
    private V: number;
    private graph: number[][];
    private readonly INF = 9999999;

    constructor(vertices: number) {
        this.V = vertices;
        this.graph = new Array(vertices).fill(0).map(() => new Array(vertices).fill(this.INF));

        for (let i = 0; i < vertices; i++) {
            this.graph[i][i] = 0;
        }
    }

    public addEdge(u: number, v: number, weight: number): void {
        this.graph[u][v] = weight;
    }

    public solve(): number[][] {
        const dist = this.graph.map(row => [...row]);

        for (let k = 0; k < this.V; k++) {
            for (let i = 0; i < this.V; i++) {
                for (let j = 0; j < this.V; j++) {
                    if (dist[i][k] !== this.INF && dist[k][j] !== this.INF) {
                        if (dist[i][k] + dist[k][j] < dist[i][j]) {
                            dist[i][j] = dist[i][k] + dist[k][j];
                        }
                    }
                }
            }
        }

        for (let i = 0; i < this.V; i++) {
            if (dist[i][i] < 0) {
                throw new Error("Negative Weight Cycle Detected!");
            }
        }

        return dist;
    }
}

// --- CI/CD Automated Test ---
const fw = new FloydWarshall(4);

fw.addEdge(0, 1, 5);
fw.addEdge(0, 3, 10);
fw.addEdge(1, 2, 3);
fw.addEdge(2, 3, 1);

const shortestPaths = fw.solve();

const pass1 = shortestPaths[0][3] === 9;
const pass2 = shortestPaths[1][3] === 4;
const pass3 = shortestPaths[3][0] === 9999999;

if (pass1 && pass2 && pass3) {
    console.log("TypeScript Floyd-Warshall All-Pairs Shortest Path Test Passed!");
} else {
    process.exit(1);
}