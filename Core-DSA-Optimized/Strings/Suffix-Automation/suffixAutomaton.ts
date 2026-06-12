class State {
    public length: number;
    public link: number;
    public transitions: Map<string, number>;

    constructor(length: number = 0, link: number = -1) {
        this.length = length;
        this.link = link;
        this.transitions = new Map();
    }
}

export class SuffixAutomaton {
    private states: State[];
    private last: number;
    public size: number;

    constructor(text: string) {
        this.states = [new State(0, -1)];
        this.last = 0;
        this.size = 1;

        for (const char of text) {
            this.extend(char);
        }
    }

    private extend(char: string): void {
        const cur = this.size++;
        this.states.push(new State(this.states[this.last].length + 1));

        let p = this.last;
        while (p !== -1 && !this.states[p].transitions.has(char)) {
            this.states[p].transitions.set(char, cur);
            p = this.states[p].link;
        }

        if (p === -1) {
            this.states[cur].link = 0;
        } else {
            const q = this.states[p].transitions.get(char)!;
            if (this.states[p].length + 1 === this.states[q].length) {
                this.states[cur].link = q;
            } else {
                const clone = this.size++;
                const cloneState = new State(this.states[p].length + 1, this.states[q].link);
                // Copy transitions
                for (const [key, val] of this.states[q].transitions.entries()) {
                    cloneState.transitions.set(key, val);
                }
                this.states.push(cloneState);

                while (p !== -1 && this.states[p].transitions.get(char) === q) {
                    this.states[p].transitions.set(char, clone);
                    p = this.states[p].link;
                }

                this.states[q].link = clone;
                this.states[cur].link = clone;
            }
        }
        this.last = cur;
    }

    public contains(pattern: string): boolean {
        let currentState = 0;
        for (const char of pattern) {
            if (!this.states[currentState].transitions.has(char)) {
                return false;
            }
            currentState = this.states[currentState].transitions.get(char)!;
        }
        return true;
    }
}

const text = "banana";
const sa = new SuffixAutomaton(text);

const p1 = sa.size <= 2 * text.length - 1;
const p2 = sa.contains("nana") === true;
const p3 = sa.contains("ban") === true;
const p4 = sa.contains("apple") === false;

if (p1 && p2 && p3 && p4) {
    console.log("TypeScript Suffix Automaton Test Passed! O(N) Substring Indexing Verified.");
} else {
    process.exit(1);
}