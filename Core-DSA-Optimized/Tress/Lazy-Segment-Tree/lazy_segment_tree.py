class LazySegmentTree:
    def __init__(self, size):
        self.n = size
        self.tree = [0] * (4 * size)
        self.lazy = [0] * (4 * size)

    def _push(self, node, start, end):
        if self.lazy[node] != 0:
            self.tree[node] += self.lazy[node] * (end - start + 1)
            if start != end:
                self.lazy[node * 2] += self.lazy[node]
                self.lazy[node * 2 + 1] += self.lazy[node]
            self.lazy[node] = 0

    def _update_range(self, node, start, end, l, r, val):
        self._push(node, start, end)
        if start > end or start > r or end < l:
            return

        if start >= l and end <= r:
            self.lazy[node] += val
            self._push(node, start, end)
            return

        mid = (start + end) // 2
        self._update_range(node * 2, start, mid, l, r, val)
        self._update_range(node * 2 + 1, mid + 1, end, l, r, val)
        self.tree[node] = self.tree[node * 2] + self.tree[node * 2 + 1]

    def _query_range(self, node, start, end, l, r):
        self._push(node, start, end)
        if start > end or start > r or end < l:
            return 0

        if start >= l and end <= r:
            return self.tree[node]

        mid = (start + end) // 2
        p1 = self._query_range(node * 2, start, mid, l, r)
        p2 = self._query_range(node * 2 + 1, mid + 1, end, l, r)
        return p1 + p2

    def update(self, l, r, val):
        self._update_range(1, 0, self.n - 1, l, r, val)

    def query(self, l, r):
        return self._query_range(1, 0, self.n - 1, l, r)

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    st = LazySegmentTree(5)
    st.update(1, 3, 10)
    st.update(2, 4, 5)
    
    res = st.query(3, 4)
    assert res == 20, f"Expected 20, got {res}"
    print("Python Lazy Segment Tree Test Passed!")