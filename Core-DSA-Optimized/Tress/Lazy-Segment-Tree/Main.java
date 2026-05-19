public class Main {
    static class LazySegmentTree {
        private int n;
        private long[] tree;
        private long[] lazy;

        public LazySegmentTree(int size) {
            this.n = size;
            this.tree = new long[4 * size];
            this.lazy = new long[4 * size];
        }

        private void push(int node, int start, int end) {
            if (lazy[node] != 0) {
                tree[node] += lazy[node] * (end - start + 1);
                if (start != end) {
                    lazy[node * 2] += lazy[node];
                    lazy[node * 2 + 1] += lazy[node];
                }
                lazy[node] = 0;
            }
        }

        private void updateRange(int node, int start, int end, int l, int r, long val) {
            push(node, start, end);
            if (start > end || start > r || end < l) return;

            if (start >= l && end <= r) {
                lazy[node] += val;
                push(node, start, end);
                return;
            }

            int mid = (start + end) / 2;
            updateRange(node * 2, start, mid, l, r, val);
            updateRange(node * 2 + 1, mid + 1, end, l, r, val);
            tree[node] = tree[node * 2] + tree[node * 2 + 1];
        }

        private long queryRange(int node, int start, int end, int l, int r) {
            push(node, start, end);
            if (start > end || start > r || end < l) return 0;

            if (start >= l && end <= r) return tree[node];

            int mid = (start + end) / 2;
            long p1 = queryRange(node * 2, start, mid, l, r);
            long p2 = queryRange(node * 2 + 1, mid + 1, end, l, r);
            return p1 + p2;
        }

        public void update(int l, int r, long val) {
            updateRange(1, 0, n - 1, l, r, val);
        }

        public long query(int l, int r) {
            return queryRange(1, 0, n - 1, l, r);
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        LazySegmentTree st = new LazySegmentTree(5);
        st.update(1, 3, 10);
        st.update(2, 4, 5);

        if (st.query(3, 4) == 20) {
            System.out.println("Java Lazy Segment Tree Test Passed!");
        } else {
            System.exit(1);
        }
    }
}