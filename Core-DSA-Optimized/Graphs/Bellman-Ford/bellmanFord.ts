class Edge {
    constructor(public u: number, public v: number, public weight: number) {}
}

export class BellmanFord {
    private V: number;
    private edges: Edge[];
    private readonly INF = 99999999;

    constructor(vertices: number) {
        this.V = vertices;
        this.edges = [];
    }

    public addEdge(u: number, v: number, weight: number): void {
        this.edges.push(new Edge(u, v, weight));
    }

    public solve(source: number): number[] {
        const dist = new Array(this.V).fill(this.INF);
        dist[source] = 0;

        // Step 1: Relax edges V-1 times
        for (let i = 1; i < this.V; i++) {
            let isUpdated = false; // Early stopping optimization
            
            for (const edge of this.edges) {
                if (dist[edge.u] !== this.INF && dist[edge.u] + edge.weight < dist[edge.v]) {
                    dist[edge.v] = dist[edge.u] + edge.weight;
                    isUpdated = true;
                }
            }

            if (!isUpdated) break;
        }

        // Step 2: Check for negative-weight cycles
        for (const edge of this.edges) {
            if (dist[edge.u] !== this.INF && dist[edge.u] + edge.weight < dist[edge.v]) {
                throw new Error("Graph contains a negative weight cycle!");
            }
        }

        return dist;
    }
}

// --- CI/CD Automated Test ---
const bf = new BellmanFord(5);
bf.addEdge(0, 1, -1);
bf.addEdge(0, 2, 4);
bf.addEdge(1, 2, 3);
bf.addEdge(1, 3, 2);
bf.addEdge(1, 4, 2);
bf.addEdge(3, 2, 5);
bf.addEdge(3, 1, 1);
bf.addEdge(4, 3, -3);

const shortestPaths = bf.solve(0);

if (shortestPaths[1] === -1 && shortestPaths[3] === -2 && shortestPaths[2] === 3) {
    console.log("TypeScript Bellman-Ford Shortest Path Test Passed!");
} else {
    process.exit(1);
}

// Cycle test
const cycleBf = new BellmanFord(3);
cycleBf.addEdge(0, 1, 1);
cycleBf.addEdge(1, 2, -1);
cycleBf.addEdge(2, 0, -1);

try {
    cycleBf.solve(0);
    process.exit(1);
} catch (e) {
    console.log("Negative cycle successfully detected and aborted.");
}