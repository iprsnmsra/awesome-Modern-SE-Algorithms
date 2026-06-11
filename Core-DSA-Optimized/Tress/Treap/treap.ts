class TreapNode {
    public key: number;
    public priority: number;
    public left: TreapNode | null = null;
    public right: TreapNode | null = null;

    constructor(key: number) {
        this.key = key;
        this.priority = Math.random();
    }
}

export class Treap {
    public root: TreapNode | null = null;

    private rightRotate(y: TreapNode): TreapNode {
        const x = y.left!;
        const T2 = x.right;
        x.right = y;
        y.left = T2;
        return x;
    }

    private leftRotate(x: TreapNode): TreapNode {
        const y = x.right!;
        const T2 = y.left;
        y.left = x;
        x.right = T2;
        return y;
    }

    private insertNode(node: TreapNode | null, key: number): TreapNode {
        if (node === null) return new TreapNode(key);

        if (key < node.key) {
            node.left = this.insertNode(node.left, key);
            if (node.left.priority > node.priority) {
                node = this.rightRotate(node);
            }
        } else if (key > node.key) {
            node.right = this.insertNode(node.right, key);
            if (node.right.priority > node.priority) {
                node = this.leftRotate(node);
            }
        }
        return node;
    }

    public insert(key: number): void {
        this.root = this.insertNode(this.root, key);
    }

    private deleteNode(node: TreapNode | null, key: number): TreapNode | null {
        if (node === null) return null;

        if (key < node.key) {
            node.left = this.deleteNode(node.left, key);
        } else if (key > node.key) {
            node.right = this.deleteNode(node.right, key);
        } else {
            if (node.left === null && node.right === null) return null;
            if (node.left === null) return node.right;
            if (node.right === null) return node.left;

            if (node.left.priority < node.right.priority) {
                node = this.leftRotate(node);
                node.left = this.deleteNode(node.left, key);
            } else {
                node = this.rightRotate(node);
                node.right = this.deleteNode(node.right, key);
            }
        }
        return node;
    }

    public delete(key: number): void {
        this.root = this.deleteNode(this.root, key);
    }

    public search(key: number): boolean {
        let curr = this.root;
        while (curr !== null) {
            if (curr.key === key) return true;
            if (key < curr.key) curr = curr.left;
            else curr = curr.right;
        }
        return false;
    }
}

// --- CI/CD Automated Test ---
const treap = new Treap();
for (let i = 1; i <= 7; i++) treap.insert(i);

const p1 = treap.search(4) === true;
const p2 = treap.search(10) === false;

treap.delete(4);
const p3 = treap.search(4) === false;

// We check if it's not a linked list (root shouldn't be 1 unless we are astronomically unlucky)
const p4 = treap.root !== null && treap.root.key !== 1;

if (p1 && p2 && p3 && p4) {
    console.log(`TypeScript Treap Test Passed! (Root balanced to: ${treap.root!.key})`);
} else {
    process.exit(1);
}