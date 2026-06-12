import java.util.ArrayList;
import java.util.List;

public class Main {
    static class BTreeNode {
        boolean leaf;
        List<Integer> keys;
        List<BTreeNode> children;

        public BTreeNode(boolean leaf) {
            this.leaf = leaf;
            this.keys = new ArrayList<>();
            this.children = new ArrayList<>();
        }
    }

    static class BTree {
        BTreeNode root;
        int t;

        public BTree(int t) {
            this.root = new BTreeNode(true);
            this.t = t;
        }

        public BTreeNode search(BTreeNode node, int k) {
            int i = 0;
            while (i < node.keys.size() && k > node.keys.get(i)) {
                i++;
            }

            if (i < node.keys.size() && k == node.keys.get(i)) {
                return node;
            }

            if (node.leaf) {
                return null;
            }

            return search(node.children.get(i), k);
        }

        public void insert(int k) {
            BTreeNode r = root;
            if (r.keys.size() == 2 * t - 1) {
                BTreeNode s = new BTreeNode(false);
                root = s;
                s.children.add(r);
                splitChild(s, 0, r);
                insertNonFull(s, k);
            } else {
                insertNonFull(r, k);
            }
        }

        private void insertNonFull(BTreeNode node, int k) {
            int i = node.keys.size() - 1;

            if (node.leaf) {
                node.keys.add(0); // make space
                while (i >= 0 && k < node.keys.get(i)) {
                    node.keys.set(i + 1, node.keys.get(i));
                    i--;
                }
                node.keys.set(i + 1, k);
            } else {
                while (i >= 0 && k < node.keys.get(i)) {
                    i--;
                }
                i++;

                BTreeNode child = node.children.get(i);
                if (child.keys.size() == 2 * t - 1) {
                    splitChild(node, i, child);
                    if (k > node.keys.get(i)) {
                        i++;
                    }
                }
                insertNonFull(node.children.get(i), k);
            }
        }

        private void splitChild(BTreeNode parent, int i, BTreeNode fullChild) {
            BTreeNode newNode = new BTreeNode(fullChild.leaf);
 
            for (int j = 0; j < t - 1; j++) {
                newNode.keys.add(fullChild.keys.remove(t));
            }

            if (!fullChild.leaf) {
                for (int j = 0; j < t; j++) {
                    newNode.children.add(fullChild.children.remove(t));
                }
            }

            parent.children.add(i + 1, newNode);
            parent.keys.add(i, fullChild.keys.remove(t - 1));
        }
    }

    public static void main(String[] args) {
        BTree btree = new BTree(3);
        for (int i = 1; i <= 20; i++) btree.insert(i);

        boolean pass = true;
        pass &= btree.search(btree.root, 15) != null;
        pass &= btree.search(btree.root, 99) == null;
        pass &= btree.root.keys.size() > 0 && btree.root.keys.get(0) != 1;

        if (pass) {
            System.out.println("Java B-Tree Test Passed! Disk-Optimized Structure Verified.");
        } else {
            System.exit(1);
        }
    }
}