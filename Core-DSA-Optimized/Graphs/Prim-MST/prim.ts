// A minimal, high-performance Min-Heap for single-file zero-dependency execution
class MinHeap {
    private heap: { node: number, weight: number }[] = [];

    public push(node: number, weight: number): void {
        this.heap.push({ node, weight });
        this.bubbleUp(this.heap.length - 1);
    }

    public pop(): { node: number, weight: number } | undefined {
        if (this.heap.length === 0) return undefined;
        if (this.heap.length === 1) return this.heap.pop();

        const top = this.heap[0];
        this.heap[0] = this.heap.pop()!;
        this.sinkDown(0);
        return top;
    }

    public isEmpty(): boolean {
        return this.heap.length === 0;
    }

    private bubbleUp(idx: number): void {
        const element = this.heap[idx];
        while (idx > 0) {
            const parentIdx = Math.floor((idx - 1) / 2);
            const parent = this.heap[parentIdx];
            if (element.weight >= parent.weight) break;
            this.heap[parentIdx] = element;
            this.heap[idx] = parent;
            idx = parentIdx;
        }
    }

    private sinkDown(idx: number): void {
        const length = this.heap.length;
        const element = this.heap[idx];
        while (true) {
            const leftChildIdx = 2 * idx + 1;
            const rightChildIdx = 2 * idx + 2;
            let swapIdx = null;

            if (leftChildIdx < length) {
                if (this.heap[leftChildIdx].weight < element.weight) {
                    swapIdx = leftChildIdx;
                }
            }
            if (rightChildIdx < length) {
                const compareWeight = swapIdx === null ? element.weight : this.heap[leftChildIdx].weight;
                if (this.heap[rightChildIdx].weight < compareWeight) {
                    swapIdx = rightChildIdx;
                }
            }

            if (swapIdx === null) break;
            this.heap[idx] = this.heap[swapIdx];
            this.heap[swapIdx] = element;
            idx = swapIdx;
        }
    }
}

class Edge {
    constructor(public toNode: number, public weight: number) {}
}

export class PrimMST {
    private V: number;
    private adj: Map<number, Edge[]>;

    constructor(vertices: number) {
        this.V = vertices;
        this.adj = new Map();
        for (let i = 0; i < vertices; i++) {
            this.adj.set(i, []);
        }
    }

    public addEdge(u: number, v: number, weight: number): void {
        this.adj.get(u)!.push(new Edge(v, weight));
        this.adj.get(v)!.push(new Edge(u, weight));
    }

    public solve(): number {
        const minHeap = new MinHeap();
        const visited = new Array(this.V).fill(false);
        let minCost = 0;
        let edgesUsed = 0;

        minHeap.push(0, 0);

        while (!minHeap.isEmpty() && edgesUsed < this.V) {
            const current = minHeap.pop()!;
            const u = current.node;

            if (visited[u]) continue;

            visited[u] = true;
            minCost += current.weight;
            edgesUsed++;

            const neighbors = this.adj.get(u)!;
            for (const neighbor of neighbors) {
                if (!visited[neighbor.toNode]) {
                    minHeap.push(neighbor.toNode, neighbor.weight);
                }
            }
        }

        if (edgesUsed !== this.V) {
            throw new Error("Graph is disconnected!");
        }

        return minCost;
    }
}

// --- CI/CD Automated Test ---
const prim = new PrimMST(4);
prim.addEdge(0, 1, 10);
prim.addEdge(0, 2, 6);
prim.addEdge(0, 3, 5);
prim.addEdge(1, 3, 15);
prim.addEdge(2, 3, 4);

const totalCost = prim.solve();

if (totalCost === 19) {
    console.log(`TypeScript Prim's Algorithm Test Passed! Minimum Network Cost: ${totalCost}`);
} else {
    process.exit(1);
}