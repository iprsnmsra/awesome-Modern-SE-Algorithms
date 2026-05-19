import java.util.*;

public class Main {
    static class TarjanSCC {
        private int id = 0;
        private int[] ids, low;
        private boolean[] onStack;
        private Stack<Integer> stack = new Stack<>();
        private List<List<Integer>> sccs = new ArrayList<>();
        private List<List<Integer>> graph;

        public TarjanSCC(int n, List<List<Integer>> graph) {
            this.graph = graph;
            ids = new int[n];
            Arrays.fill(ids, -1);
            low = new int[n];
            onStack = new boolean[n];
        }

        private void dfs(int at) {
            stack.push(at);
            onStack[at] = true;
            ids[at] = low[at] = id++;

            for (int to : graph.get(at)) {
                if (ids[to] == -1) dfs(to);
                if (onStack[to]) low[at] = Math.min(low[at], low[to]);
            }

            if (ids[at] == low[at]) {
                List<Integer> scc = new ArrayList<>();
                int node = -1;
                while (node != at) {
                    node = stack.pop();
                    onStack[node] = false;
                    scc.add(node);
                }
                sccs.add(scc);
            }
        }

        public List<List<Integer>> findSCCs() {
            for (int i = 0; i < ids.length; i++) {
                if (ids[i] == -1) dfs(i);
            }
            return sccs;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        List<List<Integer>> graph = Arrays.asList(
            Arrays.asList(1), Arrays.asList(2), Arrays.asList(0), 
            Arrays.asList(4), new ArrayList<>()
        );
        TarjanSCC tarjan = new TarjanSCC(5, graph);
        List<List<Integer>> sccs = tarjan.findSCCs();
        
        if (sccs.size() == 3) {
            System.out.println("Java Tarjan SCC Test Passed!");
        } else {
            System.exit(1);
        }
    }
}