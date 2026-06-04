import java.util.ArrayList;
import java.util.List;

public class Main {
    static class Edge {
        int u, v, weight;
        public Edge(int u, int v, int weight) {
            this.u = u; this.v = v; this.weight = weight;
        }
    }

    static class BellmanFord {
        private int V;
        private List<Edge> edges;
        private final int INF = 99999999;

        public BellmanFord(int vertices) {
            this.V = vertices;
            this.edges = new ArrayList<>();
        }

        public void addEdge(int u, int v, int weight) {
            edges.add(new Edge(u, v, weight));
        }

        public int[] solve(int source) {
            int[] dist = new int[V];
            for (int i = 0; i < V; i++) dist[i] = INF;
            dist[source] = 0;

            for (int i = 1; i < V; i++) {
                boolean isUpdated = false;
                for (Edge edge : edges) {
                    if (dist[edge.u] != INF && dist[edge.u] + edge.weight < dist[edge.v]) {
                        dist[edge.v] = dist[edge.u] + edge.weight;
                        isUpdated = true;
                    }
                }
                if (!isUpdated) break;
            }

            for (Edge edge : edges) {
                if (dist[edge.u] != INF && dist[edge.u] + edge.weight < dist[edge.v]) {
                    throw new RuntimeException("Graph contains a negative weight cycle!");
                }
            }

            return dist;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        BellmanFord bf = new BellmanFord(5);
        bf.addEdge(0, 1, -1);
        bf.addEdge(0, 2, 4);
        bf.addEdge(1, 2, 3);
        bf.addEdge(1, 3, 2);
        bf.addEdge(1, 4, 2);
        bf.addEdge(3, 2, 5);
        bf.addEdge(3, 1, 1);
        bf.addEdge(4, 3, -3);

        int[] shortestPaths = bf.solve(0);

        boolean pass = shortestPaths[1] == -1 && 
                       shortestPaths[3] == -2 && 
                       shortestPaths[2] == 3;

        if (pass) {
            System.out.println("Java Bellman-Ford Shortest Path Test Passed!");
        } else {
            System.exit(1);
        }

        BellmanFord cycleBf = new BellmanFord(3);
        cycleBf.addEdge(0, 1, 1);
        cycleBf.addEdge(1, 2, -1);
        cycleBf.addEdge(2, 0, -1);

        try {
            cycleBf.solve(0);
            System.exit(1);
        } catch (RuntimeException e) {
            System.out.println("Negative cycle successfully detected and aborted.");
        }
    }
}