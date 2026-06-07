import java.util.ArrayList;
import java.util.List;
import java.util.PriorityQueue;

public class Main {
    static class Edge implements Comparable<Edge> {
        int toNode;
        int weight;

        public Edge(int toNode, int weight) {
            this.toNode = toNode;
            this.weight = weight;
        }

        @Override
        public int compareTo(Edge other) {
            return Integer.compare(this.weight, other.weight);
        }
    }

    static class PrimMST {
        private int V;
        private List<List<Edge>> adj;

        public PrimMST(int vertices) {
            this.V = vertices;
            this.adj = new ArrayList<>(vertices);
            for (int i = 0; i < vertices; i++) {
                adj.add(new ArrayList<>());
            }
        }

        public void addEdge(int u, int v, int weight) {
            adj.get(u).add(new Edge(v, weight));
            adj.get(v).add(new Edge(u, weight));
        }

        public int solve() {
            PriorityQueue<Edge> minHeap = new PriorityQueue<>();
            boolean[] visited = new boolean[V];
            int minCost = 0;
            int edgesUsed = 0;

            minHeap.offer(new Edge(0, 0));

            while (!minHeap.isEmpty() && edgesUsed < V) {
                Edge current = minHeap.poll();
                int u = current.toNode;

                if (visited[u]) continue;

                visited[u] = true;
                minCost += current.weight;
                edgesUsed++;

                for (Edge neighbor : adj.get(u)) {
                    if (!visited[neighbor.toNode]) {
                        minHeap.offer(neighbor);
                    }
                }
            }

            if (edgesUsed != V) {
                throw new RuntimeException("Graph is disconnected!");
            }

            return minCost;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        PrimMST prim = new PrimMST(4);
        prim.addEdge(0, 1, 10);
        prim.addEdge(0, 2, 6);
        prim.addEdge(0, 3, 5);
        prim.addEdge(1, 3, 15);
        prim.addEdge(2, 3, 4);

        int totalCost = prim.solve();

        if (totalCost == 19) {
            System.out.println("Java Prim's Algorithm Test Passed! Minimum Network Cost: " + totalCost);
        } else {
            System.exit(1);
        }
    }
}