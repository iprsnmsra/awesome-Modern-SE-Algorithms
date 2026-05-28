using System;

public class Program {
    class CaveGenerator {
        int width, height;
        double fillProbability;
        public int[,] map;
        Random rand = new Random();

        public CaveGenerator(int width, int height, double fillProbability) {
            this.width = width;
            this.height = height;
            this.fillProbability = fillProbability;
            this.map = GenerateRandomMap();
        }

        private int[,] GenerateRandomMap() {
            int[,] grid = new int[width, height];
            for (int x = 0; x < width; x++) {
                for (int y = 0; y < height; y++) {
                    if (x == 0 || x == width - 1 || y == 0 || y == height - 1) {
                        grid[x, y] = 1;
                    } else {
                        grid[x, y] = rand.NextDouble() < fillProbability ? 1 : 0;
                    }
                }
            }
            return grid;
        }

        private int GetSurroundingWallCount(int[,] grid, int gridX, int gridY) {
            int wallCount = 0;
            for (int neighborX = gridX - 1; neighborX <= gridX + 1; neighborX++) {
                for (int neighborY = gridY - 1; neighborY <= gridY + 1; neighborY++) {
                    if (neighborX >= 0 && neighborX < width && neighborY >= 0 && neighborY < height) {
                        if (neighborX != gridX || neighborY != gridY) {
                            wallCount += grid[neighborX, neighborY];
                        }
                    } else {
                        wallCount++;
                    }
                }
            }
            return wallCount;
        }

        public void SmoothMap() {
            int[,] newMap = new int[width, height];

            for (int x = 0; x < width; x++) {
                for (int y = 0; y < height; y++) {
                    int neighborWalls = GetSurroundingWallCount(map, x, y);

                    if (neighborWalls > 4) {
                        newMap[x, y] = 1;
                    } else if (neighborWalls < 4) {
                        newMap[x, y] = 0;
                    } else {
                        newMap[x, y] = map[x, y];
                    }
                }
            }
            map = newMap;
        }

        public void PrintMap() {
            for (int y = 0; y < height; y++) {
                for (int x = 0; x < width; x++) {
                    Console.Write(map[x, y] == 1 ? "# " : ". ");
                }
                Console.WriteLine();
            }
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var cave = new CaveGenerator(30, 15, 0.45);

        for (int i = 0; i < 5; i++) {
            cave.SmoothMap();
        }

        cave.PrintMap();

        if (cave.map[0, 0] == 1) {
            Console.WriteLine("\nC# Cellular Automata Cave Gen Test Passed!");
            return 0;
        }
        return 1;
    }
}