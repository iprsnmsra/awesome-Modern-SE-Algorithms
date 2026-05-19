#include <iostream>
#include <vector>
#include <cassert>

class LazySegmentTree {
private:
    int n;
    std::vector<long long> tree;
    std::vector<long long> lazy;

    void push(int node, int start, int end) {
        if (lazy[node] != 0) {
            tree[node] += lazy[node] * (end - start + 1);
            if (start != end) {
                lazy[node * 2] += lazy[node];
                lazy[node * 2 + 1] += lazy[node];
            }
            lazy[node] = 0;
        }
    }

    void updateRange(int node, int start, int end, int l, int r, long long val) {
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

    long long queryRange(int node, int start, int end, int l, int r) {
        push(node, start, end);
        if (start > end || start > r || end < l) return 0;
        
        if (start >= l && end <= r) return tree[node];

        int mid = (start + end) / 2;
        long long p1 = queryRange(node * 2, start, mid, l, r);
        long long p2 = queryRange(node * 2 + 1, mid + 1, end, l, r);
        return p1 + p2;
    }

public:
    LazySegmentTree(int size) {
        n = size;
        tree.assign(4 * n, 0);
        lazy.assign(4 * n, 0);
    }

    void update(int l, int r, long long val) {
        updateRange(1, 0, n - 1, l, r, val);
    }

    long long query(int l, int r) {
        return queryRange(1, 0, n - 1, l, r);
    }
};

// --- CI/CD Automated Test ---
int main() {
    LazySegmentTree st(5); // Array size 5: [0,0,0,0,0]
    
    st.update(1, 3, 10); // Add 10 to indices 1, 2, 3. Array: [0, 10, 10, 10, 0]
    st.update(2, 4, 5);  // Add 5 to indices 2, 3, 4.  Array: [0, 10, 15, 15, 5]
    
    assert(st.query(3, 4) == 20); // Indices 3 (15) + 4 (5) = 20
    
    std::cout << "C++ Lazy Segment Tree Test Passed!\n";
    return 0;
}