#include <iostream>
#include <vector>
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
        // Path Compression
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    bool unionSets(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);

        if (rootX == rootY) return false;

        // Union by Rank
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

    bool connected(int x, int y) {
        return find(x) == find(y);
    }
};

// --- CI/CD Automated Test ---
int main() {
    UnionFind uf(5);

    uf.unionSets(0, 1);
    uf.unionSets(1, 2);
    uf.unionSets(3, 4);

    assert(uf.connected(0, 2) == true);
    assert(uf.connected(0, 3) == false);

    uf.unionSets(2, 4);
    assert(uf.connected(0, 3) == true);

    cout << "C++ Union-Find Test Passed!\n";
    return 0;
}