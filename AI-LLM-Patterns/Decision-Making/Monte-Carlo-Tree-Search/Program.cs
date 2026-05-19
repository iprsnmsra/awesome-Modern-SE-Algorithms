using System;
using System.Collections.Generic;
using System.Linq;

public class Program {
    class GameState {
        public int Total { get; }
        public GameState(int total) { Total = total; }
        public List<int> GetLegalMoves() => Total < 5 ? new List<int> { 1, 2 } : new List<int>();
        public GameState ApplyMove(int move) => new GameState(Total + move);
        public bool IsTerminal() => Total >= 5;
        public double GetResult() => Total == 5 ? 1.0 : 0.0;
    }

    class MCTSNode {
        public GameState State { get; }
        public MCTSNode Parent { get; }
        public int? Move { get; }
        public List<MCTSNode> Children { get; } = new List<MCTSNode>();
        public double Wins { get; private set; }
        public int Visits { get; private set; }
        public List<int> UntriedMoves { get; }

        public MCTSNode(GameState state, MCTSNode parent, int? move) {
            State = state;
            Parent = parent;
            Move = move;
            UntriedMoves = state.GetLegalMoves();
        }

        public MCTSNode UctSelectChild() {
            double c = 1.41;
            return Children.OrderByDescending(child => 
                (child.Wins / child.Visits) + c * Math.Sqrt(Math.Log(Visits) / child.Visits)
            ).First();
        }

        public MCTSNode Expand() {
            int move = UntriedMoves[UntriedMoves.Count - 1];
            UntriedMoves.RemoveAt(UntriedMoves.Count - 1);
            var child = new MCTSNode(State.ApplyMove(move), this, move);
            Children.Add(child);
            return child;
        }

        public void Backpropagate(double result) {
            Visits++;
            Wins += result;
            Parent?.Backpropagate(result);
        }
    }

    static int RunMCTS(GameState rootState, int iterations) {
        var root = new MCTSNode(rootState, null, null);
        var rand = new Random();

        for (int i = 0; i < iterations; i++) {
            var node = root;
            var state = new GameState(rootState.Total);

            while (node.UntriedMoves.Count == 0 && node.Children.Count > 0) {
                node = node.UctSelectChild();
                state = state.ApplyMove(node.Move.Value);
            }
            if (node.UntriedMoves.Count > 0) {
                node = node.Expand();
                state = state.ApplyMove(node.Move.Value);
            }
            while (!state.IsTerminal()) {
                var moves = state.GetLegalMoves();
                state = state.ApplyMove(moves[rand.Next(moves.Count)]);
            }
            node.Backpropagate(state.GetResult());
        }
        return root.Children.OrderByDescending(c => c.Visits).First().Move.Value;
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        int optimalMove = RunMCTS(new GameState(3), 500);
        if (optimalMove == 2) {
            Console.WriteLine("C# MCTS Test Passed!");
            return 0;
        }
        return 1;
    }
}