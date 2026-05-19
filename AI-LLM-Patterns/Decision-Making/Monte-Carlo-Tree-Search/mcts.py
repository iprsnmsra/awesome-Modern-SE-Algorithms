import math
import random

class GameState:
    def __init__(self, current_total=0):
        self.current_total = current_total

    def get_legal_moves(self):
        return [1, 2] if self.current_total < 5 else []

    def apply_move(self, move):
        return GameState(self.current_total + move)

    def is_terminal(self):
        return self.current_total >= 5

    def get_result(self):
        # Win if exactly 5, lose if overshoot
        return 1.0 if self.current_total == 5 else 0.0

class MCTSNode:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = state.get_legal_moves()

    def uct_select_child(self):
        c = 1.41
        return max(self.children, key=lambda child: 
            (child.wins / child.visits) + c * math.sqrt(math.log(self.visits) / child.visits)
        )

    def expand(self):
        move = self.untried_moves.pop()
        next_state = self.state.apply_move(move)
        child = MCTSNode(next_state, parent=self, move=move)
        self.children.append(child)
        return child

    def backpropagate(self, result):
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(result)

def run_mcts(root_state, iterations=1000):
    root = MCTSNode(root_state)
    for _ in range(iterations):
        node = root
        state = GameState(root_state.current_total)

        # Select
        while not node.untried_moves and node.children:
            node = node.uct_select_child()
            state = state.apply_move(node.move)

        # Expand
        if node.untried_moves:
            node = node.expand()
            state = state.apply_move(node.move)

        # Simulate
        while not state.is_terminal():
            state = state.apply_move(random.choice(state.get_legal_moves()))

        # Backpropagate
        node.backpropagate(state.get_result())

    return max(root.children, key=lambda c: c.visits).move

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    # Game: Start at 3. Target is 5. Legal moves: +1, +2.
    # The optimal move is clearly +2.
    best_move = run_mcts(GameState(3), iterations=500)
    assert best_move == 2, f"AI made wrong move: {best_move}"
    print("Python MCTS Test Passed!")