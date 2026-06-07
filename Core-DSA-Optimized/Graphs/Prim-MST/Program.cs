using System;
using System.Collections.Generic;

public class Program {
    public class Edge {
        public int ToNode { get; set; }
        public int Weight { get; set; }
        
        public Edge(int toNode, int weight) {
            ToNode = toNode;
            Weight = weight;
        }
    }

    public class PrimMST {
        private int V;
        private List<List<Edge>> adj;

        public PrimMST(int vertices) {
            this.V = vertices;
            this.adj = new List<List<Edge>>(vertices);
            for (int i = 0; i < vertices; i++) {
                adj.Add(new List<Edge>());
            }
        }

        public void AddEdge(int u, int v, int weight) {
            adj[u].Add(new Edge(v, weight));
            adj[v].Add(new Edge(u, weight));
        }

        public int Solve() {
            // Using .NET 6+ PriorityQueue
            var minHeap = new PriorityQueue<Edge, int>();
            bool[] visited = new bool[V];
            int minCost = 0;
            int edgesUsed = 0;

            var startEdge = new Edge(0, 0);
            minHeap.Enqueue(startEdge, startEdge.Weight);

            while (minHeap.Count > 0 && edgesUsed < V) {
                Edge current = minHeap.Dequeue();
                int u = current.ToNode;

                if (visited[u]) continue;

                visited[u] = true;
                minCost += current.Weight;
                edgesUsed++;

                foreach (Edge neighbor in adj[u]) {
                    if (!visited[neighbor.ToNode]) {
                        minHeap.Enqueue(neighbor, neighbor.Weight);
                    }
                }
            }

            if (edgesUsed != V) {
                throw new Exception("Graph is disconnected!");
            }

            return minCost;
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var prim = new PrimMST(4);
        prim.AddEdge(0, 1, 10);
        prim.AddEdge(0, 2, 6);
        prim.AddEdge(0, 3, 5);
        prim.AddEdge(1, 3, 15);
        prim.AddEdge(2, 3, 4);

        int totalCost = prim.Solve();

        if (totalCost == 19) {
            Console.WriteLine($"C# Prim's Algorithm Test Passed! Minimum Network Cost: {totalCost}");
            return 0;
        }
        return 1;
    }
}