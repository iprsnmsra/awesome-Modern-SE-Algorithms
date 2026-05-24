class Boid {
    constructor(public x: number, public y: number, public vx: number, public vy: number) {}
}

export class SwarmSimulation {
    private boids: Boid[];
    private visualRange: number;

    constructor(boids: Boid[], visualRange: number = 50.0) {
        this.boids = boids;
        this.visualRange = visualRange;
    }

    private distance(b1: Boid, b2: Boid): number {
        return Math.sqrt(Math.pow(b1.x - b2.x, 2) + Math.pow(b1.y - b2.y, 2));
    }

    public tick(): void {
        const newVelocities: { vx: number, vy: number }[] = [];

        for (const boid of this.boids) {
            let cx = 0, cy = 0;
            let vxAvg = 0, vyAvg = 0;
            let sx = 0, sy = 0;
            let neighbors = 0;

            for (const other of this.boids) {
                if (boid === other) continue;

                const dist = this.distance(boid, other);
                if (dist < this.visualRange) {
                    cx += other.x;
                    cy += other.y;
                    
                    vxAvg += other.vx;
                    vyAvg += other.vy;

                    if (dist < 20.0) {
                        sx += boid.x - other.x;
                        sy += boid.y - other.y;
                    }
                    neighbors++;
                }
            }

            let newVx = boid.vx;
            let newVy = boid.vy;

            if (neighbors > 0) {
                cx /= neighbors;
                cy /= neighbors;
                vxAvg /= neighbors;
                vyAvg /= neighbors;

                newVx += (cx - boid.x) * 0.01 + (vxAvg - boid.vx) * 0.05 + sx * 0.1;
                newVy += (cy - boid.y) * 0.01 + (vyAvg - boid.vy) * 0.05 + sy * 0.1;
            }

            newVelocities.push({ vx: newVx, vy: newVy });
        }

        for (let i = 0; i < this.boids.length; i++) {
            this.boids[i].vx = newVelocities[i].vx;
            this.boids[i].vy = newVelocities[i].vy;
            this.boids[i].x += this.boids[i].vx;
            this.boids[i].y += this.boids[i].vy;
        }
    }
}

// --- CI/CD Automated Test ---
const flock = [
    new Boid(0.0, 0.0, 1.0, 0.0),
    new Boid(5.0, 5.0, 0.0, 1.0),
    new Boid(-5.0, 5.0, -1.0, 1.0)
];

const sim = new SwarmSimulation(flock);
const initialX = flock[0].x;

sim.tick();

if (flock[0].x !== initialX) {
    console.log("TypeScript Boids Swarm Intelligence Test Passed!");
} else {
    process.exit(1);
}