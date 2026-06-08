#include <iostream>
#include <cassert>

using namespace std;

const bool RED = true;
const bool BLACK = false;

struct Node {
    int val;
    bool color;
    Node* left;
    Node* right;
    Node* parent;

    Node(int v) : val(v), color(RED), left(nullptr), right(nullptr), parent(nullptr) {}
};

class RedBlackTree {
private:
    Node* NIL;

    void leftRotate(Node* x) {
        Node* y = x->right;
        x->right = y->left;
        if (y->left != NIL) y->left->parent = x;
        
        y->parent = x->parent;
        if (x->parent == NIL) {
            root = y;
        } else if (x == x->parent->left) {
            x->parent->left = y;
        } else {
            x->parent->right = y;
        }
        y->left = x;
        x->parent = y;
    }

    void rightRotate(Node* x) {
        Node* y = x->left;
        x->left = y->right;
        if (y->right != NIL) y->right->parent = x;
        
        y->parent = x->parent;
        if (x->parent == NIL) {
            root = y;
        } else if (x == x->parent->right) {
            x->parent->right = y;
        } else {
            x->parent->left = y;
        }
        y->right = x;
        x->parent = y;
    }

    void insertFixup(Node* z) {
        while (z->parent->color == RED) {
            if (z->parent == z->parent->parent->left) {
                Node* y = z->parent->parent->right;
                if (y->color == RED) {
                    z->parent->color = BLACK;
                    y->color = BLACK;
                    z->parent->parent->color = RED;
                    z = z->parent->parent;
                } else {
                    if (z == z->parent->right) {
                        z = z->parent;
                        leftRotate(z);
                    }
                    z->parent->color = BLACK;
                    z->parent->parent->color = RED;
                    rightRotate(z->parent->parent);
                }
            } else {
                Node* y = z->parent->parent->left;
                if (y->color == RED) {
                    z->parent->color = BLACK;
                    y->color = BLACK;
                    z->parent->parent->color = RED;
                    z = z->parent->parent;
                } else {
                    if (z == z->parent->left) {
                        z = z->parent;
                        rightRotate(z);
                    }
                    z->parent->color = BLACK;
                    z->parent->parent->color = RED;
                    leftRotate(z->parent->parent);
                }
            }
        }
        root->color = BLACK;
    }

public:
    Node* root;

    RedBlackTree() {
        NIL = new Node(0);
        NIL->color = BLACK;
        root = NIL;
    }

    void insert(int val) {
        Node* z = new Node(val);
        z->left = NIL;
        z->right = NIL;

        Node* y = NIL;
        Node* x = root;

        while (x != NIL) {
            y = x;
            if (z->val < x->val) x = x->left;
            else x = x->right;
        }

        z->parent = y;
        if (y == NIL) root = z;
        else if (z->val < y->val) y->left = z;
        else y->right = z;

        if (z->parent == NIL) {
            z->color = BLACK;
            return;
        }
        if (z->parent->parent == NIL) return;

        insertFixup(z);
    }

    bool search(int val) {
        Node* current = root;
        while (current != NIL) {
            if (val == current->val) return true;
            if (val < current->val) current = current->left;
            else current = current->right;
        }
        return false;
    }
};

// --- CI/CD Automated Test ---
int main() {
    RedBlackTree rbt;
    for (int i = 1; i <= 7; i++) rbt.insert(i);

    assert(rbt.search(4) == true);
    assert(rbt.search(10) == false);
    assert(rbt.root->val != 1);

    cout << "C++ Red-Black Tree Test Passed! (Root balanced to: " << rbt.root->val << ")\n";
    return 0;
}