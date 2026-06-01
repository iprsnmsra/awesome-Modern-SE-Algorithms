using System;

public class Program {
    public class UnionFind {
        private int[] parent;
        private int[] rank;

        public UnionFind(int size) {
            parent = new int[size];
            rank = new int[size];
            for (int i = 0; i < size; i++) {
                parent[i] = i;
                rank[i] = 1;
            }
        }

        public int Find(int x) {
            // Path Compression
            if (parent[x] != x) {
                parent[x] = Find(parent[x]);
            }
            return parent[x];
        }

        public bool Union(int x, int y) {
            int rootX = Find(x);
            int rootY = Find(y);

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

        public bool Connected(int x, int y) {
            return Find(x) == Find(y);
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var uf = new UnionFind(5);

        uf.Union(0, 1);
        uf.Union(1, 2);
        uf.Union(3, 4);

        if (uf.Connected(0, 2) && !uf.Connected(0, 3)) {
            uf.Union(2, 4);
            if (uf.Connected(0, 3)) {
                Console.WriteLine("C# Union-Find Test Passed!");
                return 0;
            }
        }
        
        return 1;
    }
}