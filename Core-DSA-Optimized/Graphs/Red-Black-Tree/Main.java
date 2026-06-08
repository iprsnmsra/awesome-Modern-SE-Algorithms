public class Main {
    private static final boolean RED = true;
    private static final boolean BLACK = false;

    static class Node {
        int val;
        boolean color;
        Node left, right, parent;

        public Node(int val) {
            this.val = val;
            this.color = RED;
        }
    }

    static class RedBlackTree {
        private final Node NIL;
        public Node root;

        public RedBlackTree() {
            NIL = new Node(0);
            NIL.color = BLACK;
            root = NIL;
        }

        private void leftRotate(Node x) {
            Node y = x.right;
            x.right = y.left;
            if (y.left != NIL) y.left.parent = x;
            
            y.parent = x.parent;
            if (x.parent == NIL) {
                root = y;
            } else if (x == x.parent.left) {
                x.parent.left = y;
            } else {
                x.parent.right = y;
            }
            y.left = x;
            x.parent = y;
        }

        private void rightRotate(Node x) {
            Node y = x.left;
            x.left = y.right;
            if (y.right != NIL) y.right.parent = x;
            
            y.parent = x.parent;
            if (x.parent == NIL) {
                root = y;
            } else if (x == x.parent.right) {
                x.parent.right = y;
            } else {
                x.parent.left = y;
            }
            y.right = x;
            x.parent = y;
        }

        private void insertFixup(Node z) {
            while (z.parent.color == RED) {
                if (z.parent == z.parent.parent.left) {
                    Node y = z.parent.parent.right;
                    if (y.color == RED) {
                        z.parent.color = BLACK;
                        y.color = BLACK;
                        z.parent.parent.color = RED;
                        z = z.parent.parent;
                    } else {
                        if (z == z.parent.right) {
                            z = z.parent;
                            leftRotate(z);
                        }
                        z.parent.color = BLACK;
                        z.parent.parent.color = RED;
                        rightRotate(z.parent.parent);
                    }
                } else {
                    Node y = z.parent.parent.left;
                    if (y.color == RED) {
                        z.parent.color = BLACK;
                        y.color = BLACK;
                        z.parent.parent.color = RED;
                        z = z.parent.parent;
                    } else {
                        if (z == z.parent.left) {
                            z = z.parent;
                            rightRotate(z);
                        }
                        z.parent.color = BLACK;
                        z.parent.parent.color = RED;
                        leftRotate(z.parent.parent);
                    }
                }
            }
            root.color = BLACK;
        }

        public void insert(int val) {
            Node z = new Node(val);
            z.left = NIL;
            z.right = NIL;

            Node y = NIL;
            Node x = root;

            while (x != NIL) {
                y = x;
                if (z.val < x.val) x = x.left;
                else x = x.right;
            }

            z.parent = y;
            if (y == NIL) root = z;
            else if (z.val < y.val) y.left = z;
            else y.right = z;

            if (z.parent == NIL) {
                z.color = BLACK;
                return;
            }
            if (z.parent.parent == NIL) return;

            insertFixup(z);
        }

        public boolean search(int val) {
            Node current = root;
            while (current != NIL) {
                if (val == current.val) return true;
                if (val < current.val) current = current.left;
                else current = current.right;
            }
            return false;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        RedBlackTree rbt = new RedBlackTree();
        for (int i = 1; i <= 7; i++) rbt.insert(i);

        boolean pass = rbt.search(4) == true && 
                       rbt.search(10) == false && 
                       rbt.root.val != 1;

        if (pass) {
            System.out.println("Java Red-Black Tree Test Passed! (Root balanced to: " + rbt.root.val + ")");
        } else {
            System.exit(1);
        }
    }
}