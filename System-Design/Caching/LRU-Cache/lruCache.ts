export class LRUCache<K, V> {
    private capacity: number;
    private cache: Map<K, V>;

    constructor(capacity: number) {
        this.capacity = capacity;
        this.cache = new Map();
    }

    get(key: K): V | -1 {
        if (!this.cache.has(key)) return -1;
        const val = this.cache.get(key)!;
        this.cache.delete(key);
        this.cache.set(key, val); 
        return val;
    }

    put(key: K, value: V): void {
        if (this.cache.has(key)) {
            this.cache.delete(key);
        } else if (this.cache.size >= this.capacity) {
            const oldestKey = this.cache.keys().next().value;
            this.cache.delete(oldestKey!);
        }
        this.cache.set(key, value);
    }
}

const lru = new LRUCache<number, number>(2);
lru.put(1, 10);
lru.put(2, 20);
const getOne = lru.get(1); 
lru.put(3, 30); 

if (getOne === 10 && lru.get(2) === -1) {
    console.log("TypeScript LRU Cache Test Passed!");
} else {
    process.exit(1);
}