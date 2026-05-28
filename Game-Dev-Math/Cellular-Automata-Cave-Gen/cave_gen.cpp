#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <cassert>

using namespace std;

class CaveGenerator {
private:
    int width, height;
    double fillProbability;

    vector<vector<int>> generateRandomMap() {
        vector<vector<int>> grid(width, vector<int>(height));
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                if (x == 0 || x == width - 1 || y == 0 || y == height - 1) {
                    grid[x][y] = 1;
                } else {
                    grid[x][y] = ((double)rand() / RAND_MAX) < fillProbability ? 1 : 0;
                }
            }
        }
        return grid;
    }

    int getSurroundingWallCount(const vector<vector<int>>& grid, int gridX, int gridY) {
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

public:
    vector<vector<int>> map;

    CaveGenerator(int w, int h, double fillProb) : width(w), height(h), fillProbability(fillProb) {
        srand(time(nullptr));
        map = generateRandomMap();
    }

    void smoothMap() {
        vector<vector<int>> newMap(width, vector<int>(height));

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

    void printMap() {
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                cout << (map[x][y] == 1 ? "# " : ". ");
            }
            cout << "\n";
        }
    }
};

// --- CI/CD Automated Test ---
int main() {
    CaveGenerator cave(30, 15, 0.45);

    for (int i = 0; i < 5; i++) {
        cave.smoothMap();
    }

    cave.printMap();

    assert(cave.map[0][0] == 1);
    
    cout << "\nC++ Cellular Automata Cave Gen Test Passed!\n";
    return 0;
}