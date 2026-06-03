class FloydWarshall:
    # Use a large number for Infinity to prevent integer overflow during addition
    INF = 9999999

    def __init__(self, vertices: int):
        self.V = vertices
        # Initialize an empty V x V matrix
        self.graph = [[self.INF for _ in range(vertices)] for _ in range(vertices)]
        
        # Distance from a node to itself is always 0
        for i in range(vertices):
            self.graph[i][i] = 0

    def add_edge(self, u: int, v: int, weight: int):
        self.graph[u][v] = weight

    def solve(self) -> list[list[int]]:
        # Create a copy of the graph to store the shortest paths
        dist = [row[:] for row in self.graph]

        # Dynamic Programming: k is the intermediate node
        for k in range(self.V):
            # i is the source node
            for i in range(self.V):
                # j is the destination node
                for j in range(self.V):
                    # If routing through 'k' is shorter than the direct route, update it
                    if dist[i][k] != self.INF and dist[k][j] != self.INF:
                        if dist[i][k] + dist[k][j] < dist[i][j]:
                            dist[i][j] = dist[i][k] + dist[k][j]

        # Negative Cycle Detection
        for i in range(self.V):
            if dist[i][i] < 0:
                raise Exception("Negative Weight Cycle Detected!")

        return dist

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    # 4 Vertices (0 to 3)
    fw = FloydWarshall(4)
    
    fw.add_edge(0, 1, 5)
    fw.add_edge(0, 3, 10)
    fw.add_edge(1, 2, 3)
    fw.add_edge(2, 3, 1)
    
    shortest_paths = fw.solve()
    
    # 1. Path 0 -> 3 directly is 10. But 0 -> 1 -> 2 -> 3 is (5 + 3 + 1) = 9.
    assert shortest_paths[0][3] == 9, f"Failed! Expected 9, got {shortest_paths[0][3]}"
    
    # 2. Path 1 -> 3 is 1 -> 2 -> 3 = (3 + 1) = 4
    assert shortest_paths[1][3] == 4, f"Failed! Expected 4, got {shortest_paths[1][3]}"
    
    # 3. Path 3 -> 0 does not exist
    assert shortest_paths[3][0] == fw.INF, "Failed! Path 3->0 should be Infinity"
    
    print("Python Floyd-Warshall All-Pairs Shortest Path Test Passed!")