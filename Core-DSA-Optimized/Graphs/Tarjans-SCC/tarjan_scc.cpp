#include <iostream>
#include <vector>
#include <stack>
#include <algorithm>
#include <cassert>

class TarjanSCC {
    int id = 0;
    std::vector<int> ids, low;
    std::vector<bool> onStack;
    std::stack<int> st;
    std::vector<std::vector<int>> sccs;

    void dfs(int at, const std::vector<std::vector<int>>& graph) {
        st.push(at);
        onStack[at] = true;
        ids[at] = low[at] = id++;

        for (int to : graph[at]) {
            if (ids[to] == -1) dfs(to, graph);
            if (onStack[to]) low[at] = std::min(low[at], low[to]);
        }

        if (ids[at] == low[at]) {
            std::vector<int> scc;
            int node = -1;
            while (node != at) {
                node = st.top(); st.pop();
                onStack[node] = false;
                scc.push_back(node);
            }
            sccs.push_back(scc);
        }
    }

public:
    std::vector<std::vector<int>> findSCCs(int n, const std::vector<std::vector<int>>& graph) {
        ids.assign(n, -1);
        low.assign(n, 0);
        onStack.assign(n, false);
        
        for (int i = 0; i < n; i++) {
            if (ids[i] == -1) dfs(i, graph);
        }
        return sccs;
    }
};

// --- CI/CD Automated Test ---
int main() {
    std::vector<std::vector<int>> graph = {{1}, {2}, {0}, {4}, {}};
    TarjanSCC tarjan;
    auto sccs = tarjan.findSCCs(5, graph);
    
    assert(sccs.size() == 3);
    std::cout << "C++ Tarjan SCC Test Passed!\n";
    return 0;
}