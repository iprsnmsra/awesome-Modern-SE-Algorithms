export class CaveGenerator {
    private width: number;
    private height: number;
    private fillProbability: number;
    public map: number[][];

    constructor(width: number, height: number, fillProbability: number = 0.45) {
        this.width = width;
        this.height = height;
        this.fillProbability = fillProbability;
        this.map = this.generateRandomMap();
    }

    private generateRandomMap(): number[][] {
        const grid: number[][] = [];
        for (let x = 0; x < this.width; x++) {
            grid[x] = [];
            for (let y = 0; y < this.height; y++) {
                if (x === 0 || x === this.width - 1 || y === 0 || y === this.height - 1) {
                    grid[x][y] = 1;
                } else {
                    grid[x][y] = Math.random() < this.fillProbability ? 1 : 0;
                }
            }
        }
        return grid;
    }

    private getSurroundingWallCount(grid: number[][], gridX: number, gridY: number): number {
        let wallCount = 0;
        for (let neighborX = gridX - 1; neighborX <= gridX + 1; neighborX++) {
            for (let neighborY = gridY - 1; neighborY <= gridY + 1; neighborY++) {
                if (neighborX >= 0 && neighborX < this.width && neighborY >= 0 && neighborY < this.height) {
                    if (neighborX !== gridX || neighborY !== gridY) {
                        wallCount += grid[neighborX][neighborY];
                    }
                } else {
                    wallCount++;
                }
            }
        }
        return wallCount;
    }

    public smoothMap(): void {
        const newMap: number[][] = Array.from({ length: this.width }, () => new Array(this.height).fill(0));

        for (let x = 0; x < this.width; x++) {
            for (let y = 0; y < this.height; y++) {
                const neighborWalls = this.getSurroundingWallCount(this.map, x, y);

                if (neighborWalls > 4) {
                    newMap[x][y] = 1;
                } else if (neighborWalls < 4) {
                    newMap[x][y] = 0;
                } else {
                    newMap[x][y] = this.map[x][y];
                }
            }
        }
        this.map = newMap;
    }

    public printMap(): void {
        for (let y = 0; y < this.height; y++) {
            let line = "";
            for (let x = 0; x < this.width; x++) {
                line += this.map[x][y] === 1 ? "# " : ". ";
            }
            console.log(line);
        }
    }
}

// --- CI/CD Automated Test ---
const cave = new CaveGenerator(30, 15, 0.45);

for (let i = 0; i < 5; i++) {
    cave.smoothMap();
}

cave.printMap();

if (cave.map[0][0] === 1) {
    console.log("\nTypeScript Cellular Automata Cave Gen Test Passed!");
} else {
    process.exit(1);
}