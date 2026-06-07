import heapq

class Edge:
    def __init__(self, to_node: int, weight: int):
        self.to_node = to_node
        self.weight = weight

    # Custom comparator for the Priority Queue
    def __lt__(self, other):
        return self.weight < other.weight

class PrimMST:
    def __init__(self, vertices: int):
        self.V = vertices
        # Adjacency list representation
        self.adj = {i: [] for i in range(vertices)}

    def add_edge(self, u: int, v: int, weight: int):
        # Undirected graph
        self.adj[u].append(Edge(v, weight))
        self.adj[v].append(Edge(u, weight))

    def solve(self) -> int:
        min_heap = []
        visited = [False] * self.V
        min_cost = 0
        edges_used = 0

        # Start at node 0
        # Push a dummy edge (weight 0, to node 0) to kickstart the loop
        heapq.heappush(min_heap, Edge(0, 0))

        while min_heap and edges_used < self.V:
            current_edge = heapq.heappop(min_heap)
            u = current_edge.to_node

            # If we've already visited this node, it would create a cycle. Skip it.
            if visited[u]:
                continue

            # Mark visited and add cost
            visited[u] = True
            min_cost += current_edge.weight
            edges_used += 1

            # Push all unvisited neighbors into the Min-Heap
            for neighbor in self.adj[u]:
                if not visited[neighbor.to_node]:
                    heapq.heappush(min_heap, neighbor)

        # Safety check for disconnected graphs
        if edges_used != self.V:
            raise Exception("Graph is disconnected! Spanning tree impossible.")

        return min_cost

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    # Graph with 4 vertices (0 to 3)
    prim = PrimMST(4)
    
    prim.add_edge(0, 1, 10)
    prim.add_edge(0, 2, 6)
    prim.add_edge(0, 3, 5)
    prim.add_edge(1, 3, 15)
    prim.add_edge(2, 3, 4)
    
    total_cost = prim.solve()
    
    # The MST should pick edges: (2-3: 4), (0-3: 5), (0-1: 10) -> Total: 19
    assert total_cost == 19, f"Failed! Expected MST cost 19, got {total_cost}"
    
    print(f"Python Prim's Algorithm Test Passed! Minimum Network Cost: {total_cost}")