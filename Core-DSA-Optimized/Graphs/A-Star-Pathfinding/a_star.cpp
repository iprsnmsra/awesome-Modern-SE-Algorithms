#include <iostream>
#include <vector>
#include <queue>
#include <cmath>
#include <map>
#include <algorithm>
#include <cassert>

using namespace std;

struct Node {
    int r, c, f;
    bool operator>(const Node& other) const {
        return f > other.f; // Min-heap based on F-score
    }
    bool operator==(const Node& other) const {
        return r == other.r && c == other.c;
    }
    bool operator<(const Node& other) const {
        if (r != other.r) return r < other.r;
        return c < other.c;
    }
};

class AStar {
private:
    vector<vector<int>> grid;

    int heuristic(Node a, Node b) {
        return abs(a.r - b.r) + abs(a.c - b.c);
    }

public:
    AStar(vector<vector<int>> g) : grid(g) {}

    vector<Node> findPath(Node start, Node goal) {
        priority_queue<Node, vector<Node>, greater<Node>> openSet;
        map<Node, Node> cameFrom;
        map<Node, int> gScore;

        start.f = heuristic(start, goal);
        openSet.push(start);
        gScore[start] = 0;

        vector<pair<int, int>> dirs = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};

        while (!openSet.empty()) {
            Node current = openSet.top();
            openSet.pop();

            if (current == goal) {
                vector<Node> path;
                while (cameFrom.find(current) != cameFrom.end()) {
                    path.push_back(current);
                    current = cameFrom[current];
                }
                path.push_back(start);
                reverse(path.begin(), path.end());
                return path;
            }

            for (auto& d : dirs) {
                Node neighbor = {current.r + d.first, current.c + d.second, 0};

                if (neighbor.r >= 0 && neighbor.r < grid.size() && 
                    neighbor.c >= 0 && neighbor.c < grid[0].size() && 
                    grid[neighbor.r][neighbor.c] == 0) {
                    
                    int tentativeG = gScore[current] + 1;

                    if (gScore.find(neighbor) == gScore.end() || tentativeG < gScore[neighbor]) {
                        cameFrom[neighbor] = current;
                        gScore[neighbor] = tentativeG;
                        neighbor.f = tentativeG + heuristic(neighbor, goal);
                        openSet.push(neighbor);
                    }
                }
            }
        }
        return {}; // Empty path
    }
};

// --- CI/CD Automated Test ---
int main() {
    vector<vector<int>> maze = {
        {0, 1, 0, 0, 0},
        {0, 1, 0, 1, 0},
        {0, 0, 0, 1, 0},
        {0, 1, 1, 1, 0},
        {0, 0, 0, 0, 0}
    };

    AStar astar(maze);
    vector<Node> path = astar.findPath({0, 0, 0}, {4, 4, 0});

    assert(path.size() > 0);
    cout << "C++ A* Pathfinding Test Passed! Path Length: " << path.size() << "\n";
    return 0;
}