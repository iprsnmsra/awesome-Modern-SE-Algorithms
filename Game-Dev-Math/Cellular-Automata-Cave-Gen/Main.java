import java.util.Random;

public class Main {
    static class CaveGenerator {
        int width, height;
        double fillProbability;
        int[][] map;
        Random rand = new Random();

        public CaveGenerator(int width, int height, double fillProbability) {
            this.width = width;
            this.height = height;
            this.fillProbability = fillProbability;
            this.map = generateRandomMap();
        }

        private int[][] generateRandomMap() {
            int[][] grid = new int[width][height];
            for (int x = 0; x < width; x++) {
                for (int y = 0; y < height; y++) {
                    if (x == 0 || x == width - 1 || y == 0 || y == height - 1) {
                        grid[x][y] = 1;
                    } else {
                        grid[x][y] = rand.nextDouble() < fillProbability ? 1 : 0;
                    }
                }
            }
            return grid;
        }

        private int getSurroundingWallCount(int[][] grid, int gridX, int gridY) {
            int wallCount = 0;
            for (int neighborX = gridX - 1; neighborX <= gridX + 1; neighborX++) {
                for (int neighborY = gridY - 1; neighborY <= gridY + 1; neighborY++) {
                    if (neighborX >= 0 && neighborX < width && neighborY >= 0 && neighborY < height) {
                        if (neighborX != gridX || neighborY != gridY) {
                            wallCount += grid[neighborX][neighborY];
                        }
                    } else {
                        wallCount++;
                    }
                }
            }
            return wallCount;
        }

        public void smoothMap() {
            int[][] newMap = new int[width][height];

            for (int x = 0; x < width; x++) {
                for (int y = 0; y < height; y++) {
                    int neighborWalls = getSurroundingWallCount(map, x, y);

                    if (neighborWalls > 4) {
                        newMap[x][y] = 1;
                    } else if (neighborWalls < 4) {
                        newMap[x][y] = 0;
                    } else {
                        newMap[x][y] = map[x][y];
                    }
                }
            }
            map = newMap;
        }

        public void printMap() {
            for (int y = 0; y < height; y++) {
                StringBuilder line = new StringBuilder();
                for (int x = 0; x < width; x++) {
                    line.append(map[x][y] == 1 ? "# " : ". ");
                }
                System.out.println(line.toString());
            }
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        CaveGenerator cave = new CaveGenerator(30, 15, 0.45);

        for (int i = 0; i < 5; i++) {
            cave.smoothMap();
        }

        cave.printMap();

        if (cave.map[0][0] == 1) {
            System.out.println("\nJava Cellular Automata Cave Gen Test Passed!");
        } else {
            System.exit(1);
        }
    }
}