import { createHash } from 'crypto';

export class ConsistentHash {
    private virtualNodes: number;
    private ring: Map<number, string> = new Map();
    private sortedKeys: number[] = [];

    constructor(virtualNodes: number = 100) {
        this.virtualNodes = virtualNodes;
    }

    private hash(key: string): number {
        return parseInt(createHash('md5').update(key).digest('hex').substring(0, 8), 16);
    }

    public addServer(server: string): void {
        for (let i = 0; i < this.virtualNodes; i++) {
            const h = this.hash(`${server}#${i}`);
            this.ring.set(h, server);
            this.sortedKeys.push(h);
        }
        this.sortedKeys.sort((a, b) => a - b);
    }

    public getServer(key: string): string | null {
        if (this.ring.size === 0) return null;
        const h = this.hash(key);
        
        let left = 0, right = this.sortedKeys.length - 1;
        while (left <= right) {
            const mid = Math.floor((left + right) / 2);
            if (this.sortedKeys[mid] === h) return this.ring.get(this.sortedKeys[mid])!;
            if (this.sortedKeys[mid] < h) left = mid + 1;
            else right = mid - 1;
        }

        const targetKey = left >= this.sortedKeys.length ? this.sortedKeys[0] : this.sortedKeys[left];
        return this.ring.get(targetKey)!;
    }
}

const ch = new ConsistentHash(5);
ch.addServer("Worker_1");
ch.addServer("Worker_2");

const assignedServer = ch.getServer("Task_Alpha");
if (assignedServer === "Worker_1" || assignedServer === "Worker_2") {
    console.log("TypeScript Consistent Hashing Test Passed!");
} else {
    process.exit(1);
}