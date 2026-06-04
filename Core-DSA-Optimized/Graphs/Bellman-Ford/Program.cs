using System;
using System.Collections.Generic;

public class Program {
    public class Edge {
        public int u, v, weight;
        public Edge(int u, int v, int weight) {
            this.u = u; this.v = v; this.weight = weight;
        }
    }

    public class BellmanFord {
        private int V;
        private List<Edge> edges;
        private readonly int INF = 99999999;

        public BellmanFord(int vertices) {
            this.V = vertices;
            this.edges = new List<Edge>();
        }

        public void AddEdge(int u, int v, int weight) {
            edges.Add(new Edge(u, v, weight));
        }

        public int[] Solve(int source) {
            int[] dist = new int[V];
            for (int i = 0; i < V; i++) dist[i] = INF;
            dist[source] = 0;

            for (int i = 1; i < V; i++) {
                bool isUpdated = false;
                foreach (var edge in edges) {
                    if (dist[edge.u] != INF && dist[edge.u] + edge.weight < dist[edge.v]) {
                        dist[edge.v] = dist[edge.u] + edge.weight;
                        isUpdated = true;
                    }
                }
                if (!isUpdated) break;
            }

            foreach (var edge in edges) {
                if (dist[edge.u] != INF && dist[edge.u] + edge.weight < dist[edge.v]) {
                    throw new Exception("Graph contains a negative weight cycle!");
                }
            }

            return dist;
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var bf = new BellmanFord(5);
        bf.AddEdge(0, 1, -1);
        bf.AddEdge(0, 2, 4);
        bf.AddEdge(1, 2, 3);
        bf.AddEdge(1, 3, 2);
        bf.AddEdge(1, 4, 2);
        bf.AddEdge(3, 2, 5);
        bf.AddEdge(3, 1, 1);
        bf.AddEdge(4, 3, -3);

        int[] shortestPaths = bf.Solve(0);

        bool pass = shortestPaths[1] == -1 && 
                    shortestPaths[3] == -2 && 
                    shortestPaths[2] == 3;

        if (pass) {
            Console.WriteLine("C# Bellman-Ford Shortest Path Test Passed!");
        } else {
            return 1;
        }

        var cycleBf = new BellmanFord(3);
        cycleBf.AddEdge(0, 1, 1);
        cycleBf.AddEdge(1, 2, -1);
        cycleBf.AddEdge(2, 0, -1);

        try {
            cycleBf.Solve(0);
            return 1;
        } catch (Exception) {
            Console.WriteLine("Negative cycle successfully detected and aborted.");
            return 0;
        }
    }
}