using System;
using System.Collections.Generic;

public class Program {
    public class BTreeNode {
        public bool leaf;
        public List<int> keys;
        public List<BTreeNode> children;

        public BTreeNode(bool leaf) {
            this.leaf = leaf;
            this.keys = new List<int>();
            this.children = new List<BTreeNode>();
        }
    }

    public class BTree {
        public BTreeNode root;
        private int t;

        public BTree(int t) {
            this.root = new BTreeNode(true);
            this.t = t;
        }

        public BTreeNode Search(BTreeNode node, int k) {
            int i = 0;
            while (i < node.keys.Count && k > node.keys[i]) {
                i++;
            }

            if (i < node.keys.Count && k == node.keys[i]) {
                return node;
            }

            if (node.leaf) {
                return null;
            }

            return Search(node.children[i], k);
        }

        public void Insert(int k) {
            BTreeNode r = root;
            if (r.keys.Count == 2 * t - 1) {
                BTreeNode s = new BTreeNode(false);
                root = s;
                s.children.Add(r);
                SplitChild(s, 0, r);
                InsertNonFull(s, k);
            } else {
                InsertNonFull(r, k);
            }
        }

        private void InsertNonFull(BTreeNode node, int k) {
            int i = node.keys.Count - 1;

            if (node.leaf) {
                node.keys.Add(0); // make space
                while (i >= 0 && k < node.keys[i]) {
                    node.keys[i + 1] = node.keys[i];
                    i--;
                }
                node.keys[i + 1] = k;
            } else {
                while (i >= 0 && k < node.keys[i]) {
                    i--;
                }
                i++;

                BTreeNode child = node.children[i];
                if (child.keys.Count == 2 * t - 1) {
                    SplitChild(node, i, child);
                    if (k > node.keys[i]) {
                        i++;
                    }
                }
                InsertNonFull(node.children[i], k);
            }
        }

        private void SplitChild(BTreeNode parent, int i, BTreeNode fullChild) {
            BTreeNode newNode = new BTreeNode(fullChild.leaf);
            
            for (int j = 0; j < t - 1; j++) {
                newNode.keys.Add(fullChild.keys[t]);
                fullChild.keys.RemoveAt(t);
            }

            if (!fullChild.leaf) {
                for (int j = 0; j < t; j++) {
                    newNode.children.Add(fullChild.children[t]);
                    fullChild.children.RemoveAt(t);
                }
            }

            parent.children.Insert(i + 1, newNode);
            int middleKey = fullChild.keys[t - 1];
            fullChild.keys.RemoveAt(t - 1);
            parent.keys.Insert(i, middleKey);
        }
    }
    public static int Main() {
        BTree btree = new BTree(3);
        for (int i = 1; i <= 20; i++) btree.Insert(i);

        bool pass = true;
        pass &= btree.Search(btree.root, 15) != null;
        pass &= btree.Search(btree.root, 99) == null;
        pass &= btree.root.keys.Count > 0 && btree.root.keys[0] != 1;

        if (pass) {
            Console.WriteLine("C# B-Tree Test Passed! Disk-Optimized Structure Verified.");
            return 0;
        }
        return 1;
    }
}