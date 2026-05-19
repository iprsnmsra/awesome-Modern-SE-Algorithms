import java.util.*;

public class Main {
    static class GameState {
        int total;
        public GameState(int total) { this.total = total; }
        public List<Integer> getLegalMoves() { 
            return total < 5 ? Arrays.asList(1, 2) : new ArrayList<>(); 
        }
        public GameState applyMove(int move) { return new GameState(total + move); }
        public boolean isTerminal() { return total >= 5; }
        public double getResult() { return total == 5 ? 1.0 : 0.0; }
    }

    static class MCTSNode {
        GameState state;
        MCTSNode parent;
        Integer move;
        List<MCTSNode> children = new ArrayList<>();
        double wins = 0;
        int visits = 0;
        List<Integer> untriedMoves;

        public MCTSNode(GameState state, MCTSNode parent, Integer move) {
            this.state = state;
            this.parent = parent;
            this.move = move;
            this.untriedMoves = new ArrayList<>(state.getLegalMoves());
        }

        public MCTSNode uctSelectChild() {
            double c = 1.41;
            return Collections.max(children, Comparator.comparingDouble(child -> 
                (child.wins / child.visits) + c * Math.sqrt(Math.log(this.visits) / child.visits)
            ));
        }

        public MCTSNode expand() {
            int move = untriedMoves.remove(untriedMoves.size() - 1);
            MCTSNode child = new MCTSNode(state.applyMove(move), this, move);
            children.add(child);
            return child;
        }

        public void backpropagate(double result) {
            this.visits++;
            this.wins += result;
            if (this.parent != null) this.parent.backpropagate(result);
        }
    }

    public static int runMCTS(GameState rootState, int iterations) {
        MCTSNode root = new MCTSNode(rootState, null, null);
        Random rand = new Random();

        for (int i = 0; i < iterations; i++) {
            MCTSNode node = root;
            GameState state = new GameState(rootState.total);

            while (node.untriedMoves.isEmpty() && !node.children.isEmpty()) {
                node = node.uctSelectChild();
                state = state.applyMove(node.move);
            }
            if (!node.untriedMoves.isEmpty()) {
                node = node.expand();
                state = state.applyMove(node.move);
            }
            while (!state.isTerminal()) {
                List<Integer> moves = state.getLegalMoves();
                state = state.applyMove(moves.get(rand.nextInt(moves.size())));
            }
            node.backpropagate(state.getResult());
        }
        return Collections.max(root.children, Comparator.comparingInt(c -> c.visits)).move;
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        int optimalMove = runMCTS(new GameState(3), 500);
        if (optimalMove == 2) {
            System.out.println("Java MCTS Test Passed!");
        } else {
            System.exit(1);
        }
    }
}