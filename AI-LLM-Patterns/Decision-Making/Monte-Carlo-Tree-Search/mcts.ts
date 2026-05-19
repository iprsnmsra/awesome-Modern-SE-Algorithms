class GameState {
    constructor(public total: number = 0) {}
    getLegalMoves(): number[] { return this.total < 5 ? [1, 2] : []; }
    applyMove(move: number): GameState { return new GameState(this.total + move); }
    isTerminal(): boolean { return this.total >= 5; }
    getResult(): number { return this.total === 5 ? 1.0 : 0.0; }
}

class MCTSNode {
    children: MCTSNode[] = [];
    wins: number = 0;
    visits: number = 0;
    untriedMoves: number[];

    constructor(public state: GameState, public parent: MCTSNode | null = null, public move: number | null = null) {
        this.untriedMoves = state.getLegalMoves();
    }

    uctSelectChild(): MCTSNode {
        const c = 1.41;
        return this.children.reduce((best, child) => {
            const uct = (child.wins / child.visits) + c * Math.sqrt(Math.log(this.visits) / child.visits);
            const bestUct = (best.wins / best.visits) + c * Math.sqrt(Math.log(this.visits) / best.visits);
            return uct > bestUct ? child : best;
        });
    }

    expand(): MCTSNode {
        const move = this.untriedMoves.pop()!;
        const child = new MCTSNode(this.state.applyMove(move), this, move);
        this.children.push(child);
        return child;
    }

    backpropagate(result: number): void {
        this.visits++;
        this.wins += result;
        if (this.parent) this.parent.backpropagate(result);
    }
}

function runMCTS(rootState: GameState, iterations: number = 1000): number {
    const root = new MCTSNode(rootState);
    for (let i = 0; i < iterations; i++) {
        let node = root;
        let state = new GameState(rootState.total);

        while (node.untriedMoves.length === 0 && node.children.length > 0) {
            node = node.uctSelectChild();
            state = state.applyMove(node.move!);
        }
        if (node.untriedMoves.length > 0) {
            node = node.expand();
            state = state.applyMove(node.move!);
        }
        while (!state.isTerminal()) {
            const moves = state.getLegalMoves();
            state = state.applyMove(moves[Math.floor(Math.random() * moves.length)]);
        }
        node.backpropagate(state.getResult());
    }
    return root.children.reduce((best, child) => child.visits > best.visits ? child : best).move!;
}

// --- CI/CD Automated Test ---
const optimalMove = runMCTS(new GameState(3), 500);
if (optimalMove === 2) {
    console.log("TypeScript MCTS Test Passed!");
} else {
    process.exit(1);
}