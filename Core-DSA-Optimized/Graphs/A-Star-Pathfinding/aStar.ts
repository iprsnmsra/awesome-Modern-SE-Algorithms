type Node = { r: number, c: number };

export class AStar {
    private grid: number[][];
    private rows: number;
    private cols: number;

    constructor(grid: number[][]) {
        this.grid = grid;
        this.rows = grid.length;
        this.cols = grid[0].length;
    }

    private heuristic(a: Node, b: Node): number {
        return Math.abs(a.r - b.r) + Math.abs(a.c - b.c); // Manhattan
    }

    private hash(node: Node): string {
        return `${node.r},${node.c}`;
    }

    public findPath(start: Node, goal: Node): Node[] {
        // Priority Queue (Sorted dynamically for simplicity in single-file)
        let openSet: { f: number, node: Node }[] = [{ f: 0, node: start }];
        const cameFrom = new Map<string, Node>();
        
        const gScore = new Map<string, number>();
        gScore.set(this.hash(start), 0);

        while (openSet.length > 0) {
            openSet.sort((a, b) => a.f - b.f);
            const current = openSet.shift()!.node;

            if (current.r === goal.r && current.c === goal.c) {
                const path = [current];
                let currHash = this.hash(current);
                while (cameFrom.has(currHash)) {
                    const prev = cameFrom.get(currHash)!;
                    path.push(prev);
                    currHash = this.hash(prev);
                }
                return path.reverse();
            }

            const directions = [[0, 1], [1, 0], [0, -1], [-1, 0]];
            for (const [dr, dc] of directions) {
                const neighbor = { r: current.r + dr, c: current.c + dc };
                
                if (neighbor.r >= 0 && neighbor.r < this.rows && neighbor.c >= 0 && neighbor.c < this.cols) {
                    if (this.grid[neighbor.r][neighbor.c] === 1) continue;

                    const tentativeG = gScore.get(this.hash(current))! + 1;
                    const neighborHash = this.hash(neighbor);

                    if (!gScore.has(neighborHash) || tentativeG < gScore.get(neighborHash)!) {
                        cameFrom.set(neighborHash, current);
                        gScore.set(neighborHash, tentativeG);
                        const fScore = tentativeG + this.heuristic(neighbor, goal);
                        openSet.push({ f: fScore, node: neighbor });
                    }
                }
            }
        }
        return [];
    }
}

// --- CI/CD Automated Test ---
const maze = [
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
];

const astar = new AStar(maze);
const path = astar.findPath({r: 0, c: 0}, {r: 4, c: 4});

if (path.length > 0 && path[0].r === 0 && path[path.length - 1].r === 4) {
    console.log(`TypeScript A* Pathfinding Test Passed! Path Length: ${path.length}`);
} else {
    process.exit(1);
}