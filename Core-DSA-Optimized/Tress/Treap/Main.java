import java.util.Random;

public class Main {
    static class TreapNode {
        int key;
        double priority;
        TreapNode left, right;

        public TreapNode(int key, Random rand) {
            this.key = key;
            this.priority = rand.nextDouble();
        }
    }

    static class Treap {
        public TreapNode root;
        private Random rand;

        public Treap() {
            this.root = null;
            this.rand = new Random(42); // Seeded for deterministic testing
        }

        private TreapNode rightRotate(TreapNode y) {
            TreapNode x = y.left;
            TreapNode T2 = x.right;
            x.right = y;
            y.left = T2;
            return x;
        }

        private TreapNode leftRotate(TreapNode x) {
            TreapNode y = x.right;
            TreapNode T2 = y.left;
            y.left = x;
            x.right = T2;
            return y;
        }

        private TreapNode insert(TreapNode node, int key) {
            if (node == null) return new TreapNode(key, rand);

            if (key < node.key) {
                node.left = insert(node.left, key);
                if (node.left.priority > node.priority) {
                    node = rightRotate(node);
                }
            } else if (key > node.key) {
                node.right = insert(node.right, key);
                if (node.right.priority > node.priority) {
                    node = leftRotate(node);
                }
            }
            return node;
        }

        public void insert(int key) {
            root = insert(root, key);
        }

        private TreapNode delete(TreapNode node, int key) {
            if (node == null) return null;

            if (key < node.key) {
                node.left = delete(node.left, key);
            } else if (key > node.key) {
                node.right = delete(node.right, key);
            } else {
                if (node.left == null && node.right == null) return null;
                if (node.left == null) return node.right;
                if (node.right == null) return node.left;

                if (node.left.priority < node.right.priority) {
                    node = leftRotate(node);
                    node.left = delete(node.left, key);
                } else {
                    node = rightRotate(node);
                    node.right = delete(node.right, key);
                }
            }
            return node;
        }

        public void delete(int key) {
            root = delete(root, key);
        }

        public boolean search(int key) {
            TreapNode curr = root;
            while (curr != null) {
                if (curr.key == key) return true;
                if (key < curr.key) curr = curr.left;
                else curr = curr.right;
            }
            return false;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        Treap treap = new Treap();
        for (int i = 1; i <= 7; i++) treap.insert(i);

        boolean pass = treap.search(4) == true && treap.search(10) == false;
        
        treap.delete(4);
        pass &= treap.search(4) == false;
        
        pass &= treap.root.key != 1;

        if (pass) {
            System.out.println("Java Treap Test Passed! (Root balanced to: " + treap.root.key + ")");
        } else {
            System.exit(1);
        }
    }
}