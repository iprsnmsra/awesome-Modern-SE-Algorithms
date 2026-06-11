#include <iostream>
#include <cstdlib>
#include <cassert>

using namespace std;

struct TreapNode {
    int key;
    double priority;
    TreapNode* left;
    TreapNode* right;

    TreapNode(int k) : key(k), left(nullptr), right(nullptr) {
        priority = static_cast<double>(rand()) / RAND_MAX;
    }
};

class Treap {
private:
    TreapNode* rightRotate(TreapNode* y) {
        TreapNode* x = y->left;
        TreapNode* T2 = x->right;
        x->right = y;
        y->left = T2;
        return x;
    }

    TreapNode* leftRotate(TreapNode* x) {
        TreapNode* y = x->right;
        TreapNode* T2 = y->left;
        y->left = x;
        x->right = T2;
        return y;
    }

    TreapNode* insertNode(TreapNode* node, int key) {
        if (node == nullptr) return new TreapNode(key);

        if (key < node->key) {
            node->left = insertNode(node->left, key);
            if (node->left->priority > node->priority) {
                node = rightRotate(node);
            }
        } else if (key > node->key) {
            node->right = insertNode(node->right, key);
            if (node->right->priority > node->priority) {
                node = leftRotate(node);
            }
        }
        return node;
    }

    TreapNode* deleteNode(TreapNode* node, int key) {
        if (node == nullptr) return nullptr;

        if (key < node->key) {
            node->left = deleteNode(node->left, key);
        } else if (key > node->key) {
            node->right = deleteNode(node->right, key);
        } else {
            if (node->left == nullptr && node->right == nullptr) {
                delete node;
                return nullptr;
            }
            if (node->left == nullptr) {
                TreapNode* temp = node->right;
                delete node;
                return temp;
            }
            if (node->right == nullptr) {
                TreapNode* temp = node->left;
                delete node;
                return temp;
            }

            if (node->left->priority < node->right->priority) {
                node = leftRotate(node);
                node->left = deleteNode(node->left, key);
            } else {
                node = rightRotate(node);
                node->right = deleteNode(node->right, key);
            }
        }
        return node;
    }

    void cleanup(TreapNode* node) {
        if (node != nullptr) {
            cleanup(node->left);
            cleanup(node->right);
            delete node;
        }
    }

public:
    TreapNode* root;

    Treap() {
        root = nullptr;
        srand(42); // Deterministic testing
    }

    ~Treap() {
        cleanup(root);
    }

    void insert(int key) {
        root = insertNode(root, key);
    }

    void remove(int key) {
        root = deleteNode(root, key);
    }

    bool search(int key) {
        TreapNode* curr = root;
        while (curr != nullptr) {
            if (curr->key == key) return true;
            if (key < curr->key) curr = curr->left;
            else curr = curr->right;
        }
        return false;
    }
};

// --- CI/CD Automated Test ---
int main() {
    Treap treap;
    for (int i = 1; i <= 7; i++) treap.insert(i);

    assert(treap.search(4) == true);
    assert(treap.search(10) == false);
    assert(treap.root->key != 1);

    treap.remove(4);
    assert(treap.search(4) == false);

    cout << "C++ Treap Test Passed! (Root balanced to: " << treap.root->key << ")\n";
    return 0;
}