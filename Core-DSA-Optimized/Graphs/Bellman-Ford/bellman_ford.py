class Edge:
    def __init__(self, u: int, v: int, weight: int):
        self.u = u
        self.v = v
        self.weight = weight

class BellmanFord:
    # Using a large number to prevent float('inf') math errors in typed languages
    INF = 99999999

    def __init__(self, vertices: int):
        self.V = vertices
        self.edges = []

    def add_edge(self, u: int, v: int, weight: int):
        self.edges.append(Edge(u, v, weight))

    def solve(self, source: int) -> list[int]:
        dist = [self.INF] * self.V
        dist[source] = 0

        # Step 1: Relax all edges V - 1 times
        for _ in range(self.V - 1):
            is_updated = False # Principal Engineer Early-Stopping Optimization
            for edge in self.edges:
                if dist[edge.u] != self.INF and dist[edge.u] + edge.weight < dist[edge.v]:
                    dist[edge.v] = dist[edge.u] + edge.weight
                    is_updated = True
            
            # If no distances changed in this pass, we are already perfectly optimized
            if not is_updated:
                break

        # Step 2: Check for negative-weight cycles
        for edge in self.edges:
            if dist[edge.u] != self.INF and dist[edge.u] + edge.weight < dist[edge.v]:
                raise Exception("Graph contains a negative weight cycle!")

        return dist

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    # 5 Vertices (0 to 4)
    bf = BellmanFord(5)
    
    bf.add_edge(0, 1, -1)
    bf.add_edge(0, 2, 4)
    bf.add_edge(1, 2, 3)
    bf.add_edge(1, 3, 2)
    bf.add_edge(1, 4, 2)
    bf.add_edge(3, 2, 5)
    bf.add_edge(3, 1, 1)
    bf.add_edge(4, 3, -3)
    
    shortest_paths = bf.solve(source=0)
    
    # Path 0 -> 1 is -1
    assert shortest_paths[1] == -1, f"Expected -1, got {shortest_paths[1]}"
    
    # Path 0 -> 1 -> 4 -> 3 is -1 + 2 + -3 = -2
    assert shortest_paths[3] == -2, f"Expected -2, got {shortest_paths[3]}"
    
    # Path 0 -> 1 -> 4 -> 3 -> 2 is -1 + 2 + -3 + 5 = 3
    assert shortest_paths[2] == 3, f"Expected 3, got {shortest_paths[2]}"
    
    print("Python Bellman-Ford Shortest Path Test Passed!")
    
    # Test Negative Cycle Detection
    cycle_bf = BellmanFord(3)
    cycle_bf.add_edge(0, 1, 1)
    cycle_bf.add_edge(1, 2, -1)
    cycle_bf.add_edge(2, 0, -1) # Creates a cycle: 1 - 1 - 1 = -1
    
    try:
        cycle_bf.solve(0)
        assert False, "Failed to detect negative cycle!"
    except Exception as e:
        print("Negative cycle successfully detected and aborted.")