class LFUNode {
    public freq: number = 1;
    public prev: LFUNode | null = null;
    public next: LFUNode | null = null;

    constructor(public key: number, public val: number) {}
}

class DoublyLinkedList {
    public head: LFUNode;
    public tail: LFUNode;
    public size: number = 0;

    constructor() {
        this.head = new LFUNode(0, 0);
        this.tail = new LFUNode(0, 0);
        this.head.next = this.tail;
        this.tail.prev = this.head;
    }

    public insertHead(node: LFUNode): void {
        const nxt = this.head.next!;
        this.head.next = node;
        node.prev = this.head;
        node.next = nxt;
        nxt.prev = node;
        this.size++;
    }

    public remove(node: LFUNode): void {
        const prev = node.prev!;
        const nxt = node.next!;
        prev.next = nxt;
        nxt.prev = prev;
        this.size--;
    }

    public popTail(): LFUNode | null {
        if (this.size > 0) {
            const tailNode = this.tail.prev!;
            this.remove(tailNode);
            return tailNode;
        }
        return null;
    }
}

export class LFUCache {
    private capacity: number;
    private minFreq: number = 0;
    private keyToNode: Map<number, LFUNode> = new Map();
    private freqToList: Map<number, DoublyLinkedList> = new Map();

    constructor(capacity: number) {
        this.capacity = capacity;
    }

    private updateFreq(node: LFUNode): void {
        const oldFreq = node.freq;
        this.freqToList.get(oldFreq)!.remove(node);

        if (oldFreq === this.minFreq && this.freqToList.get(oldFreq)!.size === 0) {
            this.minFreq++;
        }

        node.freq++;
        const newFreq = node.freq;
        
        if (!this.freqToList.has(newFreq)) {
            this.freqToList.set(newFreq, new DoublyLinkedList());
        }
        this.freqToList.get(newFreq)!.insertHead(node);
    }

    public get(key: number): number {
        if (!this.keyToNode.has(key)) return -1;
        
        const node = this.keyToNode.get(key)!;
        this.updateFreq(node);
        return node.val;
    }

    public put(key: number, value: number): void {
        if (this.capacity === 0) return;

        if (this.keyToNode.has(key)) {
            const node = this.keyToNode.get(key)!;
            node.val = value;
            this.updateFreq(node);
            return;
        }

        if (this.keyToNode.size >= this.capacity) {
            const lruNode = this.freqToList.get(this.minFreq)!.popTail()!;
            this.keyToNode.delete(lruNode.key);
        }

        const newNode = new LFUNode(key, value);
        this.keyToNode.set(key, newNode);
        this.minFreq = 1;

        if (!this.freqToList.has(1)) {
            this.freqToList.set(1, new DoublyLinkedList());
        }
        this.freqToList.get(1)!.insertHead(newNode);
    }
}

// --- CI/CD Automated Test ---
const lfu = new LFUCache(2);

lfu.put(1, 1);
lfu.put(2, 2);

const p1 = lfu.get(1) === 1;

lfu.put(3, 3); // Evicts 2
const p2 = lfu.get(2) === -1;
const p3 = lfu.get(3) === 3;

lfu.put(4, 4); // Evicts 1
const p4 = lfu.get(1) === -1;
const p5 = lfu.get(3) === 3;
const p6 = lfu.get(4) === 4;

if (p1 && p2 && p3 && p4 && p5 && p6) {
    console.log("TypeScript LFU Cache Test Passed!");
} else {
    process.exit(1);
}