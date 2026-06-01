public class Main {
    static class UnionFind {
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

        public int find(int x) {
            // Path Compression
            if (parent[x] != x) {
                parent[x] = find(parent[x]);
            }
            return parent[x];
        }

        public boolean union(int x, int y) {
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

        public boolean connected(int x, int y) {
            return find(x) == find(y);
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        UnionFind uf = new UnionFind(5);

        uf.union(0, 1);
        uf.union(1, 2);
        uf.union(3, 4);

        boolean pass = uf.connected(0, 2) && !uf.connected(0, 3);
        
        uf.union(2, 4);
        pass = pass && uf.connected(0, 3);

        if (pass) {
            System.out.println("Java Union-Find Test Passed!");
        } else {
            System.exit(1);
        }
    }
}