export class SnowflakeGenerator {
    // Note: We MUST use BigInt because standard JS numbers lose precision over 53 bits.
    private readonly EPOCH = 1609459200000n;
    private readonly WORKER_ID_BITS = 5n;
    private readonly DATACENTER_ID_BITS = 5n;
    private readonly SEQUENCE_BITS = 12n;

    private readonly MAX_WORKER_ID = -1n ^ (-1n << this.WORKER_ID_BITS);
    private readonly MAX_DATACENTER_ID = -1n ^ (-1n << this.DATACENTER_ID_BITS);

    private readonly WORKER_SHIFT = this.SEQUENCE_BITS;
    private readonly DATACENTER_SHIFT = this.SEQUENCE_BITS + this.WORKER_ID_BITS;
    private readonly TIMESTAMP_SHIFT = this.SEQUENCE_BITS + this.WORKER_ID_BITS + this.DATACENTER_ID_BITS;

    private readonly SEQUENCE_MASK = -1n ^ (-1n << this.SEQUENCE_BITS);

    private datacenterId: bigint;
    private workerId: bigint;
    private sequence: bigint = 0n;
    private lastTimestamp: bigint = -1n;

    constructor(datacenterId: number, workerId: number) {
        this.datacenterId = BigInt(datacenterId);
        this.workerId = BigInt(workerId);

        if (this.datacenterId > this.MAX_DATACENTER_ID || this.datacenterId < 0n) {
            throw new Error(`Datacenter ID must be between 0 and ${this.MAX_DATACENTER_ID}`);
        }
        if (this.workerId > this.MAX_WORKER_ID || this.workerId < 0n) {
            throw new Error(`Worker ID must be between 0 and ${this.MAX_WORKER_ID}`);
        }
    }

    private currentTimeMillis(): bigint {
        return BigInt(Date.now());
    }

    public nextId(): bigint {
        let timestamp = this.currentTimeMillis();

        if (timestamp < this.lastTimestamp) {
            throw new Error("Clock moved backwards.");
        }

        if (timestamp === this.lastTimestamp) {
            this.sequence = (this.sequence + 1n) & this.SEQUENCE_MASK;
            if (this.sequence === 0n) {
                while (timestamp <= this.lastTimestamp) {
                    timestamp = this.currentTimeMillis();
                }
            }
        } else {
            this.sequence = 0n;
        }

        this.lastTimestamp = timestamp;

        return ((timestamp - this.EPOCH) << this.TIMESTAMP_SHIFT) |
               (this.datacenterId << this.DATACENTER_SHIFT) |
               (this.workerId << this.WORKER_SHIFT) |
               this.sequence;
    }
}

// --- CI/CD Automated Test ---
const generator = new SnowflakeGenerator(1, 1);
const id1 = generator.nextId();
const id2 = generator.nextId();

if (id1 !== id2 && id2 > id1) {
    console.log(`TypeScript Snowflake ID Test Passed!`);
    console.log(`Generated ID 1: ${id1.toString()}`);
    console.log(`Generated ID 2: ${id2.toString()}`);
} else {
    process.exit(1);
}