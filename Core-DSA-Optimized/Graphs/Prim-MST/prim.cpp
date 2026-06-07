#include <iostream>
#include <vector>
#include <queue>
#include <stdexcept>
#include <cassert>

using namespace std;

struct Edge {
    int toNode;
    int weight;

    Edge(int to, int w) : toNode(to), weight(w) {}

    // Overload greater-than operator for Min-Heap priority queue
    bool operator>(const Edge& other) const {
        return weight > other.weight;
    }
};

class PrimMST {
private:
    int V;
    vector<vector<Edge>> adj;

public:
    PrimMST(int vertices) : V(vertices) {
        adj.resize(vertices);
    }

    void addEdge(int u, int v, int weight) {
        adj[u].emplace_back(v, weight);
        adj[v].emplace_back(u, weight);
    }

    int solve() {
        priority_queue<Edge, vector<Edge>, greater<Edge>> minHeap;
        vector<bool> visited(V, false);
        int minCost = 0;
        int edgesUsed = 0;

        minHeap.emplace(0, 0);

        while (!minHeap.empty() && edgesUsed < V) {
            Edge current = minHeap.top();
            minHeap.pop();

            int u = current.toNode;

            if (visited[u]) continue;

            visited[u] = true;
            minCost += current.weight;
            edgesUsed++;

            for (const Edge& neighbor : adj[u]) {
                if (!visited[neighbor.toNode]) {
                    minHeap.push(neighbor);
                }
            }
        }

        if (edgesUsed != V) {
            throw runtime_error("Graph is disconnected!");
        }

        return minCost;
    }
};

// --- CI/CD Automated Test ---
int main() {
    PrimMST prim(4);
    prim.addEdge(0, 1, 10);
    prim.addEdge(0, 2, 6);
    prim.addEdge(0, 3, 5);
    prim.addEdge(1, 3, 15);
    prim.addEdge(2, 3, 4);

    int totalCost = prim.solve();

    assert(totalCost == 19);

    cout << "C++ Prim's Algorithm Test Passed! Minimum Network Cost: " << totalCost << "\n";
    return 0;
}