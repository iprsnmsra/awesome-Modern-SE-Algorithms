#include <iostream>
#include <vector>
#include <stdexcept>
#include <cassert>

using namespace std;

struct Edge {
    int u, v, weight;
    Edge(int u, int v, int w) : u(u), v(v), weight(w) {}
};

class BellmanFord {
private:
    int V;
    vector<Edge> edges;
    const int INF = 99999999;

public:
    BellmanFord(int vertices) : V(vertices) {}

    void addEdge(int u, int v, int weight) {
        edges.emplace_back(u, v, weight);
    }

    vector<int> solve(int source) {
        vector<int> dist(V, INF);
        dist[source] = 0;

        for (int i = 1; i < V; i++) {
            bool isUpdated = false;
            for (const Edge& edge : edges) {
                if (dist[edge.u] != INF && dist[edge.u] + edge.weight < dist[edge.v]) {
                    dist[edge.v] = dist[edge.u] + edge.weight;
                    isUpdated = true;
                }
            }
            if (!isUpdated) break;
        }

        for (const Edge& edge : edges) {
            if (dist[edge.u] != INF && dist[edge.u] + edge.weight < dist[edge.v]) {
                throw runtime_error("Graph contains a negative weight cycle!");
            }
        }

        return dist;
    }
};

// --- CI/CD Automated Test ---
int main() {
    BellmanFord bf(5);
    bf.addEdge(0, 1, -1);
    bf.addEdge(0, 2, 4);
    bf.addEdge(1, 2, 3);
    bf.addEdge(1, 3, 2);
    bf.addEdge(1, 4, 2);
    bf.addEdge(3, 2, 5);
    bf.addEdge(3, 1, 1);
    bf.addEdge(4, 3, -3);

    vector<int> shortestPaths = bf.solve(0);

    assert(shortestPaths[1] == -1);
    assert(shortestPaths[3] == -2);
    assert(shortestPaths[2] == 3);

    cout << "C++ Bellman-Ford Shortest Path Test Passed!\n";

    BellmanFord cycleBf(3);
    cycleBf.addEdge(0, 1, 1);
    cycleBf.addEdge(1, 2, -1);
    cycleBf.addEdge(2, 0, -1);

    try {
        cycleBf.solve(0);
        assert(false);
    } catch (const runtime_error& e) {
        cout << "Negative cycle successfully detected and aborted.\n";
    }

    return 0;
}