class Point {
    constructor(public x: number, public y: number, public userData: any = null) {}
}

class Rectangle {
    // x, y is the center. w, h are half-widths.
    constructor(public x: number, public y: number, public w: number, public h: number) {}

    contains(point: Point): boolean {
        return (point.x >= this.x - this.w && point.x <= this.x + this.w &&
                point.y >= this.y - this.h && point.y <= this.y + this.h);
    }

    intersects(range: Rectangle): boolean {
        return !(range.x - range.w > this.x + this.w ||
                 range.x + range.w < this.x - this.w ||
                 range.y - range.h > this.y + this.h ||
                 range.y + range.h < this.y - this.h);
    }
}

export class QuadTree {
    private points: Point[] = [];
    private divided: boolean = false;
    private nw!: QuadTree;
    private ne!: QuadTree;
    private sw!: QuadTree;
    private se!: QuadTree;

    constructor(private boundary: Rectangle, private capacity: number) {}

    private subdivide(): void {
        const { x, y, w, h } = this.boundary;
        this.ne = new QuadTree(new Rectangle(x + w/2, y - h/2, w/2, h/2), this.capacity);
        this.nw = new QuadTree(new Rectangle(x - w/2, y - h/2, w/2, h/2), this.capacity);
        this.se = new QuadTree(new Rectangle(x + w/2, y + h/2, w/2, h/2), this.capacity);
        this.sw = new QuadTree(new Rectangle(x - w/2, y + h/2, w/2, h/2), this.capacity);
        this.divided = true;
    }

    insert(point: Point): boolean {
        if (!this.boundary.contains(point)) return false;

        if (this.points.length < this.capacity) {
            this.points.push(point);
            return true;
        }

        if (!this.divided) this.subdivide();

        if (this.ne.insert(point)) return true;
        if (this.nw.insert(point)) return true;
        if (this.se.insert(point)) return true;
        if (this.sw.insert(point)) return true;

        return false;
    }

    query(range: Rectangle, found: Point[] = []): Point[] {
        if (!this.boundary.intersects(range)) return found;

        for (const p of this.points) {
            if (range.contains(p)) found.push(p);
        }

        if (this.divided) {
            this.nw.query(range, found);
            this.ne.query(range, found);
            this.sw.query(range, found);
            this.se.query(range, found);
        }

        return found;
    }
}

// --- CI/CD Automated Test ---
const boundary = new Rectangle(100, 100, 100, 100);
const qt = new QuadTree(boundary, 4);

qt.insert(new Point(50, 50));
qt.insert(new Point(60, 60));
qt.insert(new Point(40, 40));
qt.insert(new Point(45, 45));
qt.insert(new Point(150, 150)); 

const queryBox = new Rectangle(50, 50, 20, 20);
const results = qt.query(queryBox);

const hasDistantPoint = results.some(p => p.x === 150);

if (results.length === 4 && !hasDistantPoint) {
    console.log("TypeScript QuadTree Spatial Partitioning Test Passed!");
} else {
    process.exit(1);
}