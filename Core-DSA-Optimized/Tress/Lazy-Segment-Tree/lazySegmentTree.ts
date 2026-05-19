export class LazySegmentTree {
    private n: number;
    private tree: Float64Array;
    private lazy: Float64Array;

    constructor(size: number) {
        this.n = size;
        this.tree = new Float64Array(4 * size);
        this.lazy = new Float64Array(4 * size);
    }

    private push(node: number, start: number, end: number): void {
        if (this.lazy[node] !== 0) {
            this.tree[node] += this.lazy[node] * (end - start + 1);
            if (start !== end) {
                this.lazy[node * 2] += this.lazy[node];
                this.lazy[node * 2 + 1] += this.lazy[node];
            }
            this.lazy[node] = 0;
        }
    }

    private updateRange(node: number, start: number, end: number, l: number, r: number, val: number): void {
        this.push(node, start, end);
        if (start > end || start > r || end < l) return;

        if (start >= l && end <= r) {
            this.lazy[node] += val;
            this.push(node, start, end);
            return;
        }

        const mid = Math.floor((start + end) / 2);
        this.updateRange(node * 2, start, mid, l, r, val);
        this.updateRange(node * 2 + 1, mid + 1, end, l, r, val);
        this.tree[node] = this.tree[node * 2] + this.tree[node * 2 + 1];
    }

    private queryRange(node: number, start: number, end: number, l: number, r: number): number {
        this.push(node, start, end);
        if (start > end || start > r || end < l) return 0;

        if (start >= l && end <= r) return this.tree[node];

        const mid = Math.floor((start + end) / 2);
        const p1 = this.queryRange(node * 2, start, mid, l, r);
        const p2 = this.queryRange(node * 2 + 1, mid + 1, end, l, r);
        return p1 + p2;
    }

    public update(l: number, r: number, val: number): void {
        this.updateRange(1, 0, this.n - 1, l, r, val);
    }

    public query(l: number, r: number): number {
        return this.queryRange(1, 0, this.n - 1, l, r);
    }
}

// --- CI/CD Automated Test ---
const st = new LazySegmentTree(5);
st.update(1, 3, 10);
st.update(2, 4, 5);

if (st.query(3, 4) === 20) {
    console.log("TypeScript Lazy Segment Tree Test Passed!");
} else {
    process.exit(1);
}