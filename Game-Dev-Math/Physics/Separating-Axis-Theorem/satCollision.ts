class Vec2 {
    constructor(public x: number, public y: number) {}

    public dot(other: Vec2): number {
        return this.x * other.x + this.y * other.y;
    }

    public normalize(): Vec2 {
        const length = Math.sqrt(this.x * this.x + this.y * this.y);
        if (length === 0) return new Vec2(0, 0);
        return new Vec2(this.x / length, this.y / length);
    }
}

class Polygon {
    constructor(public vertices: Vec2[]) {}
}

export class SeparatingAxisTheorem {
    private static getAxes(poly: Polygon): Vec2[] {
        const axes: Vec2[] = [];
        const len = poly.vertices.length;

        for (let i = 0; i < len; i++) {
            const p1 = poly.vertices[i];
            const p2 = poly.vertices[(i + 1) % len];

            const edge = new Vec2(p2.x - p1.x, p2.y - p1.y);
            const normal = new Vec2(-edge.y, edge.x);
            axes.push(normal.normalize());
        }
        return axes;
    }

    private static project(poly: Polygon, axis: Vec2): { min: number, max: number } {
        let minProj = Infinity;
        let maxProj = -Infinity;

        for (const vertex of poly.vertices) {
            const projection = vertex.dot(axis);
            if (projection < minProj) minProj = projection;
            if (projection > maxProj) maxProj = projection;
        }

        return { min: minProj, max: maxProj };
    }

    public static checkCollision(poly1: Polygon, poly2: Polygon): boolean {
        const axes = [...this.getAxes(poly1), ...this.getAxes(poly2)];

        for (const axis of axes) {
            const p1 = this.project(poly1, axis);
            const p2 = this.project(poly2, axis);

            if (p1.max < p2.min || p2.max < p1.min) {
                // Gap found
                return false;
            }
        }

        return true;
    }
}

// --- CI/CD Automated Test ---
const square1 = new Polygon([
    new Vec2(1, 1), new Vec2(3, 1), 
    new Vec2(3, 3), new Vec2(1, 3)
]);

const square2Colliding = new Polygon([
    new Vec2(2.5, 1), new Vec2(4.5, 1), 
    new Vec2(4.5, 3), new Vec2(2.5, 3)
]);

const square3Safe = new Polygon([
    new Vec2(5, 5), new Vec2(7, 5), 
    new Vec2(7, 7), new Vec2(5, 7)
]);

const p1 = SeparatingAxisTheorem.checkCollision(square1, square2Colliding) === true;
const p2 = SeparatingAxisTheorem.checkCollision(square1, square3Safe) === false;

if (p1 && p2) {
    console.log("TypeScript Separating Axis Theorem (SAT) Test Passed!");
} else {
    process.exit(1);
}