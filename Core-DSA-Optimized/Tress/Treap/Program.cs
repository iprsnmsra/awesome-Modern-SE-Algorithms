using System;

public class Program {
    public class TreapNode {
        public int key;
        public double priority;
        public TreapNode left, right;

        public TreapNode(int key, Random rand) {
            this.key = key;
            this.priority = rand.NextDouble();
        }
    }

    public class Treap {
        public TreapNode root;
        private Random rand;

        public Treap() {
            root = null;
            rand = new Random(42); // Seeded for deterministic testing
        }

        private TreapNode RightRotate(TreapNode y) {
            TreapNode x = y.left;
            TreapNode T2 = x.right;
            x.right = y;
            y.left = T2;
            return x;
        }

        private TreapNode LeftRotate(TreapNode x) {
            TreapNode y = x.right;
            TreapNode T2 = y.left;
            y.left = x;
            x.right = T2;
            return y;
        }

        private TreapNode InsertNode(TreapNode node, int key) {
            if (node == null) return new TreapNode(key, rand);

            if (key < node.key) {
                node.left = InsertNode(node.left, key);
                if (node.left.priority > node.priority) {
                    node = RightRotate(node);
                }
            } else if (key > node.key) {
                node.right = InsertNode(node.right, key);
                if (node.right.priority > node.priority) {
                    node = LeftRotate(node);
                }
            }
            return node;
        }

        public void Insert(int key) {
            root = InsertNode(root, key);
        }

        private TreapNode DeleteNode(TreapNode node, int key) {
            if (node == null) return null;

            if (key < node.key) {
                node.left = DeleteNode(node.left, key);
            } else if (key > node.key) {
                node.right = DeleteNode(node.right, key);
            } else {
                if (node.left == null && node.right == null) return null;
                if (node.left == null) return node.right;
                if (node.right == null) return node.left;

                if (node.left.priority < node.right.priority) {
                    node = LeftRotate(node);
                    node.left = DeleteNode(node.left, key);
                } else {
                    node = RightRotate(node);
                    node.right = DeleteNode(node.right, key);
                }
            }
            return node;
        }

        public void Delete(int key) {
            root = DeleteNode(root, key);
        }

        public bool Search(int key) {
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
    public static int Main() {
        var treap = new Treap();
        for (int i = 1; i <= 7; i++) treap.Insert(i);

        bool pass = treap.Search(4) == true && treap.Search(10) == false;
        
        treap.Delete(4);
        pass &= treap.Search(4) == false;
        
        pass &= treap.root.key != 1;

        if (pass) {
            Console.WriteLine($"C# Treap Test Passed! (Root balanced to: {treap.root.key})");
            return 0;
        }
        return 1;
    }
}