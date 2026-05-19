using System;
using System.Collections.Generic;

public class Program {
    class TarjanSCC {
        private int id = 0;
        private int[] ids, low;
        private bool[] onStack;
        private Stack<int> stack = new Stack<int>();
        private List<List<int>> sccs = new List<List<int>>();
        private List<List<int>> graph;

        public TarjanSCC(int n, List<List<int>> graph) {
            this.graph = graph;
            ids = new int[n];
            Array.Fill(ids, -1);
            low = new int[n];
            onStack = new bool[n];
        }

        private void DFS(int at) {
            stack.Push(at);
            onStack[at] = true;
            ids[at] = low[at] = id++;

            foreach (int to in graph[at]) {
                if (ids[to] == -1) DFS(to);
                if (onStack[to]) low[at] = Math.Min(low[at], low[to]);
            }

            if (ids[at] == low[at]) {
                List<int> scc = new List<int>();
                int node = -1;
                while (node != at) {
                    node = stack.Pop();
                    onStack[node] = false;
                    scc.Add(node);
                }
                sccs.Add(scc);
            }
        }

        public List<List<int>> FindSCCs() {
            for (int i = 0; i < ids.Length; i++) {
                if (ids[i] == -1) DFS(i);
            }
            return sccs;
        }
    }
    public static int Main() {
        var graph = new List<List<int>> {
            new List<int> { 1 }, new List<int> { 2 }, new List<int> { 0 },
            new List<int> { 4 }, new List<int>()
        };
        var tarjan = new TarjanSCC(5, graph);
        var sccs = tarjan.FindSCCs();

        if (sccs.Count == 3) {
            Console.WriteLine("C# Tarjan SCC Test Passed!");
            return 0;
        }
        return 1;
    }
}