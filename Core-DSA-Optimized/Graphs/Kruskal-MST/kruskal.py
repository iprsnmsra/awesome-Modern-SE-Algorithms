class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [1] * size

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) # Path Compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False # Cycle detected

        if self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        elif self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
            
        return True

class Edge:
    def __init__(self, u: int, v: int, weight: int):
        self.u = u
        self.v = v
        self.weight = weight

class KruskalMST:
    def __init__(self, vertices: int):
        self.V = vertices
        self.edges = []

    def add_edge(self, u: int, v: int, weight: int):
        self.edges.append(Edge(u, v, weight))

    def solve(self) -> tuple[list[Edge], int]:
        # 1. Sort all edges in non-decreasing order of their weight
        self.edges.sort(key=lambda edge: edge.weight)

        uf = UnionFind(self.V)
        mst_edges = []
        min_cost = 0

        # 2. Iterate through sorted edges
        for edge in self.edges:
            # 3. If joining them does not create a cycle, add to MST
            if uf.union(edge.u, edge.v):
                mst_edges.append(edge)
                min_cost += edge.weight
                
                # 4. Early termination: A spanning tree has exactly V - 1 edges
                if len(mst_edges) == self.V - 1:
                    break

        # Safety check for disconnected graphs
        if len(mst_edges) != self.V - 1:
            raise Exception("Graph is disconnected! Spanning tree impossible.")

        return mst_edges, min_cost

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    # Graph with 4 vertices (0 to 3)
    kruskal = KruskalMST(4)
    
    kruskal.add_edge(0, 1, 10)
    kruskal.add_edge(0, 2, 6)
    kruskal.add_edge(0, 3, 5)
    kruskal.add_edge(1, 3, 15)
    kruskal.add_edge(2, 3, 4)
    
    mst, total_cost = kruskal.solve()
    
    # The MST should pick edges: (2-3: 4), (0-3: 5), (0-1: 10) -> Total: 19
    assert total_cost == 19, f"Failed! Expected MST cost 19, got {total_cost}"
    assert len(mst) == 3, "MST must have exactly V - 1 edges"
    
    print(f"Python Kruskal's Algorithm Test Passed! Minimum Network Cost: {total_cost}")