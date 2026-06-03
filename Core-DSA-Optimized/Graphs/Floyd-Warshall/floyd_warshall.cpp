#include <iostream>
#include <vector>
#include <stdexcept>
#include <cassert>

using namespace std;

class FloydWarshall {
private:
    int V;
    vector<vector<int>> graph;

public:
    const int INF = 9999999;

    FloydWarshall(int vertices) : V(vertices) {
        graph.resize(vertices, vector<int>(vertices, INF));
        for (int i = 0; i < vertices; i++) {
            graph[i][i] = 0;
        }
    }

    void addEdge(int u, int v, int weight) {
        graph[u][v] = weight;
    }

    vector<vector<int>> solve() {
        vector<vector<int>> dist = graph;

        for (int k = 0; k < V; k++) {
            for (int i = 0; i < V; i++) {
                for (int j = 0; j < V; j++) {
                    if (dist[i][k] != INF && dist[k][j] != INF) {
                        if (dist[i][k] + dist[k][j] < dist[i][j]) {
                            dist[i][j] = dist[i][k] + dist[k][j];
                        }
                    }
                }
            }
        }

        for (int i = 0; i < V; i++) {
            if (dist[i][i] < 0) {
                throw runtime_error("Negative Weight Cycle Detected!");
            }
        }

        return dist;
    }
};

// --- CI/CD Automated Test ---
int main() {
    FloydWarshall fw(4);
    
    fw.addEdge(0, 1, 5);
    fw.addEdge(0, 3, 10);
    fw.addEdge(1, 2, 3);
    fw.addEdge(2, 3, 1);
    
    vector<vector<int>> shortestPaths = fw.solve();
    
    assert(shortestPaths[0][3] == 9);
    assert(shortestPaths[1][3] == 4);
    assert(shortestPaths[3][0] == fw.INF);

    cout << "C++ Floyd-Warshall All-Pairs Shortest Path Test Passed!\n";
    return 0;
}