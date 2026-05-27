import java.util.ArrayList;
import java.util.List;

public class Main {
    static class Point {
        double x, y;
        public Point(double x, double y) { this.x = x; this.y = y; }
    }

    static class Rectangle {
        double x, y, w, h;
        public Rectangle(double x, double y, double w, double h) {
            this.x = x; this.y = y; this.w = w; this.h = h;
        }
        public boolean contains(Point p) {
            return (p.x >= x - w && p.x <= x + w && p.y >= y - h && p.y <= y + h);
        }
        public boolean intersects(Rectangle range) {
            return !(range.x - range.w > x + w || range.x + range.w < x - w ||
                     range.y - range.h > y + h || range.y + range.h < y - h);
        }
    }

    static class QuadTree {
        Rectangle boundary;
        int capacity;
        List<Point> points;
        boolean divided;
        QuadTree nw, ne, sw, se;

        public QuadTree(Rectangle boundary, int capacity) {
            this.boundary = boundary;
            this.capacity = capacity;
            this.points = new ArrayList<>();
            this.divided = false;
        }

        private void subdivide() {
            double x = boundary.x, y = boundary.y, w = boundary.w, h = boundary.h;
            ne = new QuadTree(new Rectangle(x + w/2, y - h/2, w/2, h/2), capacity);
            nw = new QuadTree(new Rectangle(x - w/2, y - h/2, w/2, h/2), capacity);
            se = new QuadTree(new Rectangle(x + w/2, y + h/2, w/2, h/2), capacity);
            sw = new QuadTree(new Rectangle(x - w/2, y + h/2, w/2, h/2), capacity);
            divided = true;
        }

        public boolean insert(Point p) {
            if (!boundary.contains(p)) return false;
            
            if (points.size() < capacity) {
                points.add(p);
                return true;
            }
            if (!divided) subdivide();
            if (ne.insert(p)) return true;
            if (nw.insert(p)) return true;
            if (se.insert(p)) return true;
            if (sw.insert(p)) return true;
            
            return false;
        }

        public List<Point> query(Rectangle range, List<Point> found) {
            if (found == null) found = new ArrayList<>();
            if (!boundary.intersects(range)) return found;

            for (Point p : points) {
                if (range.contains(p)) found.add(p);
            }

            if (divided) {
                nw.query(range, found);
                ne.query(range, found);
                sw.query(range, found);
                se.query(range, found);
            }
            return found;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        Rectangle boundary = new Rectangle(100, 100, 100, 100);
        QuadTree qt = new QuadTree(boundary, 4);

        qt.insert(new Point(50, 50));
        qt.insert(new Point(60, 60));
        qt.insert(new Point(40, 40));
        qt.insert(new Point(45, 45));
        qt.insert(new Point(150, 150));

        Rectangle queryBox = new Rectangle(50, 50, 20, 20);
        List<Point> results = qt.query(queryBox, null);

        boolean hasDistant = false;
        for (Point p : results) {
            if (p.x == 150) hasDistant = true;
        }

        if (results.size() == 4 && !hasDistant) {
            System.out.println("Java QuadTree Spatial Partitioning Test Passed!");
        } else {
            System.exit(1);
        }
    }
}