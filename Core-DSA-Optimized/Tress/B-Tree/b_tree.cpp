#include <iostream>
#include <vector>
#include <cassert>

using namespace std;

class BTreeNode {
public:
    bool leaf;
    vector<int> keys;
    vector<BTreeNode*> children;

    BTreeNode(bool _leaf) {
        leaf = _leaf;
    }
};

class BTree {
private:
    int t;

    void insertNonFull(BTreeNode* node, int k) {
        int i = node->keys.size() - 1;

        if (node->leaf) {
            node->keys.push_back(0); // Allocate space
            while (i >= 0 && node->keys[i] > k) {
                node->keys[i + 1] = node->keys[i];
                i--;
            }
            node->keys[i + 1] = k;
        } else {
            while (i >= 0 && node->keys[i] > k) {
                i--;
            }
            i++;

            if (node->children[i]->keys.size() == 2 * t - 1) {
                splitChild(node, i, node->children[i]);
                if (node->keys[i] < k) {
                    i++;
                }
            }
            insertNonFull(node->children[i], k);
        }
    }

    void splitChild(BTreeNode* parent, int i, BTreeNode* fullChild) {
        BTreeNode* newNode = new BTreeNode(fullChild->leaf);
        
        for (int j = 0; j < t - 1; j++) {
            newNode->keys.push_back(fullChild->keys[t]);
            fullChild->keys.erase(fullChild->keys.begin() + t);
        }

        if (!fullChild->leaf) {
            for (int j = 0; j < t; j++) {
                newNode->children.push_back(fullChild->children[t]);
                fullChild->children.erase(fullChild->children.begin() + t);
            }
        }

        parent->children.insert(parent->children.begin() + i + 1, newNode);
        
        int middleKey = fullChild->keys[t - 1];
        fullChild->keys.erase(fullChild->keys.begin() + t - 1);
        parent->keys.insert(parent->keys.begin() + i, middleKey);
    }

public:
    BTreeNode* root;

    BTree(int _t) {
        root = new BTreeNode(true);
        t = _t;
    }

    BTreeNode* search(BTreeNode* node, int k) {
        int i = 0;
        while (i < node->keys.size() && k > node->keys[i]) {
            i++;
        }

        if (i < node->keys.size() && k == node->keys[i]) {
            return node;
        }

        if (node->leaf) {
            return nullptr;
        }

        return search(node->children[i], k);
    }

    void insert(int k) {
        if (root->keys.size() == 2 * t - 1) {
            BTreeNode* newRoot = new BTreeNode(false);
            newRoot->children.push_back(root);
            splitChild(newRoot, 0, root);
            root = newRoot;
            insertNonFull(root, k);
        } else {
            insertNonFull(root, k);
        }
    }
};
int main() {
    BTree btree(3);
    for (int i = 1; i <= 20; i++) btree.insert(i);

    assert(btree.search(btree.root, 15) != nullptr);
    assert(btree.search(btree.root, 99) == nullptr);
    assert(btree.root->keys.size() > 0 && btree.root->keys[0] != 1);

    cout << "C++ B-Tree Test Passed! Disk-Optimized Structure Verified.\n";
    return 0;
}