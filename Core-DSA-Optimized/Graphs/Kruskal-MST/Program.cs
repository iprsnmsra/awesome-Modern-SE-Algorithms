using System;
using System.Collections.Generic;

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
            if (parent[x] != x) {
                parent[x] = Find(parent[x]);
            }
            return parent[x];
        }

        public bool Union(int x, int y) {
            int rootX = Find(x);
            int rootY = Find(y);

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

    public class Edge {
        public int u, v, weight;
        public Edge(int u, int v, int weight) {
            this.u = u; this.v = v; this.weight = weight;
        }
    }

    public class KruskalResult {
        public List<Edge> Mst { get; set; }
        public int MinCost { get; set; }
    }

    public class KruskalMST {
        private int V;
        private List<Edge> edges;

        public KruskalMST(int vertices) {
            this.V = vertices;
            this.edges = new List<Edge>();
        }

        public void AddEdge(int u, int v, int weight) {
            edges.Add(new Edge(u, v, weight));
        }

        public KruskalResult Solve() {
            edges.Sort((a, b) => a.weight.CompareTo(b.weight));

            var uf = new UnionFind(V);
            var mst = new List<Edge>();
            int minCost = 0;

            foreach (var edge in edges) {
                if (uf.Union(edge.u, edge.v)) {
                    mst.Add(edge);
                    minCost += edge.weight;

                    if (mst.Count == V - 1) break;
                }
            }

            if (mst.Count != V - 1) {
                throw new Exception("Graph is disconnected!");
            }

            return new KruskalResult { Mst = mst, MinCost = minCost };
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var kruskal = new KruskalMST(4);
        kruskal.AddEdge(0, 1, 10);
        kruskal.AddEdge(0, 2, 6);
        kruskal.AddEdge(0, 3, 5);
        kruskal.AddEdge(1, 3, 15);
        kruskal.AddEdge(2, 3, 4);

        var result = kruskal.Solve();

        if (result.MinCost == 19 && result.Mst.Count == 3) {
            Console.WriteLine($"C# Kruskal's Algorithm Test Passed! Minimum Network Cost: {result.MinCost}");
            return 0;
        }
        return 1;
    }
}