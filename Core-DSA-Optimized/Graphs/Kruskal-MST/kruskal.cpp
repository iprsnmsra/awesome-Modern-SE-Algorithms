#include <iostream>
#include <vector>
#include <algorithm>
#include <stdexcept>
#include <cassert>

using namespace std;

class UnionFind {
private:
    vector<int> parent;
    vector<int> rank;

public:
    UnionFind(int size) {
        parent.resize(size);
        rank.resize(size, 1);
        for (int i = 0; i < size; i++) {
            parent[i] = i;
        }
    }

    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]); // Path Compression
        }
        return parent[x];
    }

    bool unionSets(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);

        if (rootX == rootY) return false;

        if (rank[rootX] > rank[rootY]) {
            parent[rootY] = rootX;
        } else if (rank[rootX] < rank[rootY]) {
            parent[rootX] = rootY;
        } else {
            parent[rootY] = rootX;
            rank[rootX]++;
        }
        return true;
    }
};

struct Edge {
    int u, v, weight;
    Edge(int u, int v, int w) : u(u), v(v), weight(w) {}
};

struct KruskalResult {
    vector<Edge> mst;
    int minCost;
};

class KruskalMST {
private:
    int V;
    vector<Edge> edges;

public:
    KruskalMST(int vertices) : V(vertices) {}

    void addEdge(int u, int v, int weight) {
        edges.emplace_back(u, v, weight);
    }

    KruskalResult solve() {
        // Sort edges using a lambda comparator
        sort(edges.begin(), edges.end(), [](const Edge& a, const Edge& b) {
            return a.weight < b.weight;
        });

        UnionFind uf(V);
        vector<Edge> mst;
        int minCost = 0;

        for (const Edge& edge : edges) {
            if (uf.unionSets(edge.u, edge.v)) {
                mst.push_back(edge);
                minCost += edge.weight;

                if (mst.size() == V - 1) break;
            }
        }

        if (mst.size() != V - 1) {
            throw runtime_error("Graph is disconnected!");
        }

        return {mst, minCost};
    }
};

// --- CI/CD Automated Test ---
int main() {
    KruskalMST kruskal(4);
    kruskal.addEdge(0, 1, 10);
    kruskal.addEdge(0, 2, 6);
    kruskal.addEdge(0, 3, 5);
    kruskal.addEdge(1, 3, 15);
    kruskal.addEdge(2, 3, 4);

    KruskalResult result = kruskal.solve();

    assert(result.minCost == 19);
    assert(result.mst.size() == 3);

    cout << "C++ Kruskal's Algorithm Test Passed! Minimum Network Cost: " << result.minCost << "\n";
    return 0;
}