public class Main {
    static class FloydWarshall {
        private int V;
        private int[][] graph;
        public final int INF = 9999999;

        public FloydWarshall(int vertices) {
            this.V = vertices;
            this.graph = new int[vertices][vertices];
            
            for (int i = 0; i < vertices; i++) {
                for (int j = 0; j < vertices; j++) {
                    graph[i][j] = INF;
                }
                graph[i][i] = 0;
            }
        }

        public void addEdge(int u, int v, int weight) {
            graph[u][v] = weight;
        }

        public int[][] solve() {
            int[][] dist = new int[V][V];
            for (int i = 0; i < V; i++) {
                System.arraycopy(graph[i], 0, dist[i], 0, V);
            }

            for (int k = 0; k < V; k++) {
                for (int i = 0; i < V; i++) {
                    for (int j = 0; j < V; j++) {
                        if (dist[i][k] != INF && dist[k][j] != INF) {
                            if (dist[i][k] + dist[k][j] < dist[i][j]) {
                                dist[i][j] = dist[i][k] + dist[k][j];
                            }
                        }
                    }
                }
            }

            for (int i = 0; i < V; i++) {
                if (dist[i][i] < 0) {
                    throw new RuntimeException("Negative Weight Cycle Detected!");
                }
            }

            return dist;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        FloydWarshall fw = new FloydWarshall(4);
        
        fw.addEdge(0, 1, 5);
        fw.addEdge(0, 3, 10);
        fw.addEdge(1, 2, 3);
        fw.addEdge(2, 3, 1);
        
        int[][] shortestPaths = fw.solve();
        
        boolean pass = true;
        pass &= shortestPaths[0][3] == 9;
        pass &= shortestPaths[1][3] == 4;
        pass &= shortestPaths[3][0] == fw.INF;

        if (pass) {
            System.out.println("Java Floyd-Warshall All-Pairs Shortest Path Test Passed!");
        } else {
            System.exit(1);
        }
    }
}