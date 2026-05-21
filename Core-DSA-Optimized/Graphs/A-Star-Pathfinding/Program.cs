using System;
using System.Collections.Generic;

public class Program {
    record Node(int R, int C);

    class AStar {
        private int[][] grid;

        public AStar(int[][] grid) { this.grid = grid; }

        private int Heuristic(Node a, Node b) {
            return Math.Abs(a.R - b.R) + Math.Abs(a.C - b.C);
        }

        public List<Node> FindPath(Node start, Node goal) {
            // PriorityQueue requires .NET 6+
            var openSet = new PriorityQueue<Node, int>();
            var cameFrom = new Dictionary<Node, Node>();
            var gScore = new Dictionary<Node, int>();

            openSet.Enqueue(start, 0);
            gScore[start] = 0;

            int[][] dirs = { new[] { 0, 1 }, new[] { 1, 0 }, new[] { 0, -1 }, new[] { -1, 0 } };

            while (openSet.Count > 0) {
                Node current = openSet.Dequeue();

                if (current == goal) {
                    var path = new List<Node>();
                    while (cameFrom.ContainsKey(current)) {
                        path.Add(current);
                        current = cameFrom[current];
                    }
                    path.Add(start);
                    path.Reverse();
                    return path;
                }

                foreach (var d in dirs) {
                    var neighbor = new Node(current.R + d[0], current.C + d[1]);

                    if (neighbor.R >= 0 && neighbor.R < grid.Length && 
                        neighbor.C >= 0 && neighbor.C < grid[0].Length && 
                        grid[neighbor.R][neighbor.C] == 0) {
                        
                        int tentativeG = gScore[current] + 1;

                        if (!gScore.ContainsKey(neighbor) || tentativeG < gScore[neighbor]) {
                            cameFrom[neighbor] = current;
                            gScore[neighbor] = tentativeG;
                            int fScore = tentativeG + Heuristic(neighbor, goal);
                            openSet.Enqueue(neighbor, fScore);
                        }
                    }
                }
            }
            return new List<Node>();
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        int[][] maze = {
            new[] {0, 1, 0, 0, 0},
            new[] {0, 1, 0, 1, 0},
            new[] {0, 0, 0, 1, 0},
            new[] {0, 1, 1, 1, 0},
            new[] {0, 0, 0, 0, 0}
        };

        var astar = new AStar(maze);
        var path = astar.FindPath(new Node(0, 0), new Node(4, 4));

        if (path.Count > 0) {
            Console.WriteLine($"C# A* Pathfinding Test Passed! Path Length: {path.Count}");
            return 0;
        }
        return 1;
    }
}