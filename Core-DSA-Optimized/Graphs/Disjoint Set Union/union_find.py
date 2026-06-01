class UnionFind:
    def __init__(self, size: int):
        # Initially, every node is its own parent (its own set)
        self.parent = [i for i in range(size)]
        # Rank keeps track of the depth of the trees to optimize merging
        self.rank = [1] * size

    def find(self, x: int) -> int:
        # Path Compression
        if self.parent[x] != x:
            # Recursively find the absolute root, and link this node directly to it
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)

        # They are already in the same set
        if root_x == root_y:
            return False

        # Union by Rank: Attach the smaller tree under the taller tree
        if self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        elif self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        else:
            # If ranks are tied, pick one as root and increment its rank
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
            
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    uf = UnionFind(5) # Nodes 0 through 4
    
    # Connect 0 to 1, and 1 to 2. (0, 1, 2) are now in a set.
    uf.union(0, 1)
    uf.union(1, 2)
    
    # Connect 3 to 4. (3, 4) are now in a separate set.
    uf.union(3, 4)
    
    # 1. Verify indirect connectivity
    assert uf.connected(0, 2) == True, "Nodes 0 and 2 should be connected!"
    
    # 2. Verify disjoint sets remain isolated
    assert uf.connected(0, 3) == False, "Nodes 0 and 3 should NOT be connected!"
    
    # 3. Merge the two massive sets
    uf.union(2, 4)
    assert uf.connected(0, 3) == True, "Nodes 0 and 3 should now be connected!"
    
    print("Python Union-Find Test Passed!")