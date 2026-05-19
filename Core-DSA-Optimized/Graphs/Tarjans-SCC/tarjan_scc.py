class TarjanSCC:
    def __init__(self, n, graph):
        self.n = n
        self.graph = graph
        self.id = 0
        self.ids = [-1] * n
        self.low = [0] * n
        self.on_stack = [False] * n
        self.stack = []
        self.sccs = []

    def _dfs(self, at):
        self.stack.append(at)
        self.on_stack[at] = True
        self.ids[at] = self.low[at] = self.id
        self.id += 1

        for to in self.graph[at]:
            if self.ids[to] == -1:
                self._dfs(to)
            if self.on_stack[to]:
                self.low[at] = min(self.low[at], self.low[to])

        if self.ids[at] == self.low[at]:
            scc = []
            while True:
                node = self.stack.pop()
                self.on_stack[node] = False
                scc.append(node)
                if node == at:
                    break
            self.sccs.append(scc)

    def find_sccs(self):
        for i in range(self.n):
            if self.ids[i] == -1:
                self._dfs(i)
        return self.sccs

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    # Graph: 0->1, 1->2, 2->0 (Cluster 1) | 3->4 (Cluster 2)
    graph = [[1], [2], [0], [4], []]
    tarjan = TarjanSCC(5, graph)
    sccs = tarjan.find_sccs()
    
    assert len(sccs) == 3 # {0,1,2}, {3}, {4}
    print("Python Tarjan SCC Test Passed!")