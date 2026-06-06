import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

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
            if (parent[x] != x) {
                parent[x] = find(parent[x]);
            }
            return parent[x];
        }

        public boolean union(int x, int y) {
            int rootX = find(x);
            int rootY = find(y);

            if (rootX == rootY) return false;

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
    }

    static class Edge {
        int u, v, weight;
        public Edge(int u, int v, int weight) {
            this.u = u; this.v = v; this.weight = weight;
        }
    }

    static class KruskalResult {
        List<Edge> mst;
        int minCost;
        public KruskalResult(List<Edge> mst, int minCost) {
            this.mst = mst; this.minCost = minCost;
        }
    }

    static class KruskalMST {
        private int V;
        private List<Edge> edges;

        public KruskalMST(int vertices) {
            this.V = vertices;
            this.edges = new ArrayList<>();
        }

        public void addEdge(int u, int v, int weight) {
            edges.add(new Edge(u, v, weight));
        }

        public KruskalResult solve() {
            edges.sort(Comparator.comparingInt(e -> e.weight));

            UnionFind uf = new UnionFind(V);
            List<Edge> mst = new ArrayList<>();
            int minCost = 0;

            for (Edge edge : edges) {
                if (uf.union(edge.u, edge.v)) {
                    mst.add(edge);
                    minCost += edge.weight;
                    
                    if (mst.size() == V - 1) break;
                }
            }

            if (mst.size() != V - 1) {
                throw new RuntimeException("Graph is disconnected!");
            }

            return new KruskalResult(mst, minCost);
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        KruskalMST kruskal = new KruskalMST(4);
        kruskal.addEdge(0, 1, 10);
        kruskal.addEdge(0, 2, 6);
        kruskal.addEdge(0, 3, 5);
        kruskal.addEdge(1, 3, 15);
        kruskal.addEdge(2, 3, 4);

        KruskalResult result = kruskal.solve();

        if (result.minCost == 19 && result.mst.size() == 3) {
            System.out.println("Java Kruskal's Algorithm Test Passed! Minimum Network Cost: " + result.minCost);
        } else {
            System.exit(1);
        }
    }
}