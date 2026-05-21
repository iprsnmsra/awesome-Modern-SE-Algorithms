import java.util.*;

public class Main {
    static class Node implements Comparable<Node> {
        int r, c, f;
        public Node(int r, int c, int f) { this.r = r; this.c = c; this.f = f; }
        
        @Override
        public int compareTo(Node other) { return Integer.compare(this.f, other.f); }
        
        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (!(o instanceof Node)) return false;
            Node n = (Node) o;
            return r == n.r && c == n.c;
        }
        
        @Override
        public int hashCode() { return Objects.hash(r, c); }
    }

    static class AStar {
        private int[][] grid;

        public AStar(int[][] grid) { this.grid = grid; }

        private int heuristic(int r1, int c1, int r2, int c2) {
            return Math.abs(r1 - r2) + Math.abs(c1 - c2);
        }

        public List<Node> findPath(int[] start, int[] goal) {
            PriorityQueue<Node> openSet = new PriorityQueue<>();
            Map<Node, Node> cameFrom = new HashMap<>();
            Map<Node, Integer> gScore = new HashMap<>();

            Node startNode = new Node(start[0], start[1], 0);
            Node goalNode = new Node(goal[0], goal[1], 0);

            openSet.add(startNode);
            gScore.put(startNode, 0);

            int[][] dirs = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};

            while (!openSet.isEmpty()) {
                Node current = openSet.poll();

                if (current.equals(goalNode)) {
                    List<Node> path = new ArrayList<>();
                    while (cameFrom.containsKey(current)) {
                        path.add(current);
                        current = cameFrom.get(current);
                    }
                    path.add(startNode);
                    Collections.reverse(path);
                    return path;
                }

                for (int[] d : dirs) {
                    int nr = current.r + d[0];
                    int nc = current.c + d[1];

                    if (nr >= 0 && nr < grid.length && nc >= 0 && nc < grid[0].length && grid[nr][nc] == 0) {
                        Node neighbor = new Node(nr, nc, 0);
                        int tentativeG = gScore.get(current) + 1;

                        if (!gScore.containsKey(neighbor) || tentativeG < gScore.get(neighbor)) {
                            cameFrom.put(neighbor, current);
                            gScore.put(neighbor, tentativeG);
                            neighbor.f = tentativeG + heuristic(nr, nc, goal[0], goal[1]);
                            openSet.add(neighbor);
                        }
                    }
                }
            }
            return new ArrayList<>();
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        int[][] maze = {
            {0, 1, 0, 0, 0},
            {0, 1, 0, 1, 0},
            {0, 0, 0, 1, 0},
            {0, 1, 1, 1, 0},
            {0, 0, 0, 0, 0}
        };

        AStar astar = new AStar(maze);
        List<Node> path = astar.findPath(new int[]{0, 0}, new int[]{4, 4});

        if (!path.isEmpty()) {
            System.out.println("Java A* Pathfinding Test Passed! Path Length: " + path.size());
        } else {
            System.exit(1);
        }
    }
}