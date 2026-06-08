const RED = true;
const BLACK = false;

class RBTNode {
    public color: boolean = RED;
    public left: RBTNode;
    public right: RBTNode;
    public parent: RBTNode;

    constructor(public val: number) {
        // Pointers initialized later to point to the NIL sentinel
        this.left = this;
        this.right = this;
        this.parent = this;
    }
}

export class RedBlackTree {
    private NIL: RBTNode;
    public root: RBTNode;

    constructor() {
        this.NIL = new RBTNode(0);
        this.NIL.color = BLACK;
        this.root = this.NIL;
    }

    private leftRotate(x: RBTNode): void {
        const y = x.right;
        x.right = y.left;
        if (y.left !== this.NIL) y.left.parent = x;
        
        y.parent = x.parent;
        if (x.parent === this.NIL) {
            this.root = y;
        } else if (x === x.parent.left) {
            x.parent.left = y;
        } else {
            x.parent.right = y;
        }
        y.left = x;
        x.parent = y;
    }

    private rightRotate(x: RBTNode): void {
        const y = x.left;
        x.left = y.right;
        if (y.right !== this.NIL) y.right.parent = x;
        
        y.parent = x.parent;
        if (x.parent === this.NIL) {
            this.root = y;
        } else if (x === x.parent.right) {
            x.parent.right = y;
        } else {
            x.parent.left = y;
        }
        y.right = x;
        x.parent = y;
    }

    private insertFixup(z: RBTNode): void {
        while (z.parent.color === RED) {
            if (z.parent === z.parent.parent.left) {
                const y = z.parent.parent.right;
                if (y.color === RED) {
                    z.parent.color = BLACK;
                    y.color = BLACK;
                    z.parent.parent.color = RED;
                    z = z.parent.parent;
                } else {
                    if (z === z.parent.right) {
                        z = z.parent;
                        this.leftRotate(z);
                    }
                    z.parent.color = BLACK;
                    z.parent.parent.color = RED;
                    this.rightRotate(z.parent.parent);
                }
            } else {
                const y = z.parent.parent.left;
                if (y.color === RED) {
                    z.parent.color = BLACK;
                    y.color = BLACK;
                    z.parent.parent.color = RED;
                    z = z.parent.parent;
                } else {
                    if (z === z.parent.left) {
                        z = z.parent;
                        this.rightRotate(z);
                    }
                    z.parent.color = BLACK;
                    z.parent.parent.color = RED;
                    this.leftRotate(z.parent.parent);
                }
            }
        }
        this.root.color = BLACK;
    }

    public insert(val: number): void {
        let z = new RBTNode(val);
        z.left = this.NIL;
        z.right = this.NIL;

        let y = this.NIL;
        let x = this.root;

        while (x !== this.NIL) {
            y = x;
            if (z.val < x.val) {
                x = x.left;
            } else {
                x = x.right;
            }
        }

        z.parent = y;
        if (y === this.NIL) {
            this.root = z;
        } else if (z.val < y.val) {
            y.left = z;
        } else {
            y.right = z;
        }

        if (z.parent === this.NIL) {
            z.color = BLACK;
            return;
        }
        if (z.parent.parent === this.NIL) return;

        this.insertFixup(z);
    }

    public search(val: number): boolean {
        let current = this.root;
        while (current !== this.NIL) {
            if (val === current.val) return true;
            if (val < current.val) current = current.left;
            else current = current.right;
        }
        return false;
    }
}

// --- CI/CD Automated Test ---
const rbt = new RedBlackTree();
for (let i = 1; i <= 7; i++) rbt.insert(i);

const p1 = rbt.search(4) === true;
const p2 = rbt.search(10) === false;
const p3 = rbt.root.val !== 1;

if (p1 && p2 && p3) {
    console.log(`TypeScript Red-Black Tree Test Passed! (Root balanced to: ${rbt.root.val})`);
} else {
    process.exit(1);
}