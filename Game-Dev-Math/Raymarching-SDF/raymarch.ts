class Vector3 {
    constructor(public x: number, public y: number, public z: number) {}
}

export class Raymarcher {
    private maxSteps = 100;
    private maxDist = 100.0;
    private surfDist = 0.01;

    private sdfSphere(p: Vector3, center: Vector3, radius: number): number {
        const dx = p.x - center.x;
        const dy = p.y - center.y;
        const dz = p.z - center.z;
        return Math.sqrt(dx * dx + dy * dy + dz * dz) - radius;
    }

    private getDistance(p: Vector3): number {
        return this.sdfSphere(p, new Vector3(0, 0, 0), 2.0);
    }

    public raymarch(ro: Vector3, rd: Vector3): number {
        let distOrigin = 0.0;

        for (let i = 0; i < this.maxSteps; i++) {
            const p = new Vector3(
                ro.x + rd.x * distOrigin,
                ro.y + rd.y * distOrigin,
                ro.z + rd.z * distOrigin
            );
            
            const distScene = this.getDistance(p);
            distOrigin += distScene;

            if (distScene < this.surfDist || distOrigin > this.maxDist) {
                break;
            }
        }

        return distOrigin;
    }
}

// --- CI/CD Automated Test ---
const engine = new Raymarcher();
const rayOrigin = new Vector3(0.0, 0.0, -5.0);
const rayDirection = new Vector3(0.0, 0.0, 1.0);

const hitDistance = engine.raymarch(rayOrigin, rayDirection);

if (Math.abs(hitDistance - 3.0) < 0.05) {
    console.log(`TypeScript Raymarching SDF Test Passed! Hit distance: ${hitDistance.toFixed(4)}`);
} else {
    process.exit(1);
}