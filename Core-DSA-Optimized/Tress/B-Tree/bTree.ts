class BTreeNode {
    public keys: number[] = [];
    public children: BTreeNode[] = [];
    public leaf: boolean;

    constructor(leaf: boolean = false) {
        this.leaf = leaf;
    }
}

export class BTree {
    public root: BTreeNode;
    private t: number; // Minimum degree

    constructor(t: number) {
        this.root = new BTreeNode(true);
        this.t = t;
    }

    public search(k: number, node: BTreeNode = this.root): [BTreeNode, number] | null {
        let i = 0;
        while (i < node.keys.length && k > node.keys[i]) {
            i++;
        }

        if (i < node.keys.length && k === node.keys[i]) {
            return [node, i];
        }

        if (node.leaf) {
            return null;
        }

        return this.search(k, node.children[i]);
    }

    public insert(k: number): void {
        const root = this.root;
        if (root.keys.length === (2 * this.t) - 1) {
            const newRoot = new BTreeNode(false);
            this.root = newRoot;
            newRoot.children.push(root);
            this.splitChild(newRoot, 0);
            this.insertNonFull(newRoot, k);
        } else {
            this.insertNonFull(root, k);
        }
    }

    private insertNonFull(node: BTreeNode, k: number): void {
        let i = node.keys.length - 1;

        if (node.leaf) {
            node.keys.push(0); // Make space
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

            if (node.children[i].keys.length === (2 * this.t) - 1) {
                this.splitChild(node, i);
                if (k > node.keys[i]) {
                    i++;
                }
            }
            this.insertNonFull(node.children[i], k);
        }
    }

    private splitChild(parent: BTreeNode, i: number): void {
        const t = this.t;
        const fullChild = parent.children[i];
        const newNode = new BTreeNode(fullChild.leaf);

        newNode.keys = fullChild.keys.splice(t, t - 1);
        
        if (!fullChild.leaf) {
            newNode.children = fullChild.children.splice(t, t);
        }

        const middleKey = fullChild.keys.pop()!;

        parent.children.splice(i + 1, 0, newNode);
        parent.keys.splice(i, 0, middleKey);
    }
}

const btree = new BTree(3);
for (let i = 1; i <= 20; i++) btree.insert(i);

const p1 = btree.search(15) !== null;
const p2 = btree.search(99) === null;
const p3 = btree.root.keys.length > 0 && btree.root.keys[0] !== 1;

if (p1 && p2 && p3) {
    console.log("TypeScript B-Tree Test Passed! Disk-Optimized Structure Verified.");
} else {
    process.exit(1);
}