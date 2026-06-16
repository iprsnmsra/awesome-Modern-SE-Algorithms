import java.util.ArrayList;
import java.util.List;

public class Main {
    static class Vector {
        double x, y;
        public Vector(double x, double y) {
            this.x = x; this.y = y;
        }
        public double dot(Vector other) {
            return this.x * other.x + this.y * other.y;
        }
        public Vector normalize() {
            double length = Math.sqrt(x * x + y * y);
            if (length == 0) return new Vector(0, 0);
            return new Vector(x / length, y / length);
        }
    }

    static class Polygon {
        List<Vector> vertices;
        public Polygon(List<Vector> vertices) {
            this.vertices = vertices;
        }
    }

    static class SeparatingAxisTheorem {
        private static List<Vector> getAxes(Polygon poly) {
            List<Vector> axes = new ArrayList<>();
            int n = poly.vertices.size();
            for (int i = 0; i < n; i++) {
                Vector p1 = poly.vertices.get(i);
                Vector p2 = poly.vertices.get((i + 1) % n);
                
                Vector edge = new Vector(p2.x - p1.x, p2.y - p1.y);
                Vector normal = new Vector(-edge.y, edge.x);
                axes.add(normal.normalize());
            }
            return axes;
        }

        private static double[] project(Polygon poly, Vector axis) {
            double min = Double.POSITIVE_INFINITY;
            double max = Double.NEGATIVE_INFINITY;
            
            for (Vector vertex : poly.vertices) {
                double projection = vertex.dot(axis);
                if (projection < min) min = projection;
                if (projection > max) max = projection;
            }
            return new double[]{min, max};
        }

        public static boolean checkCollision(Polygon poly1, Polygon poly2) {
            List<Vector> axes = new ArrayList<>();
            axes.addAll(getAxes(poly1));
            axes.addAll(getAxes(poly2));
            
            for (Vector axis : axes) {
                double[] p1 = project(poly1, axis);
                double[] p2 = project(poly2, axis);
                
                if (p1[1] < p2[0] || p2[1] < p1[0]) {
                    return false; // Gap found
                }
            }
            return true;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        List<Vector> v1 = new ArrayList<>();
        v1.add(new Vector(1, 1)); v1.add(new Vector(3, 1));
        v1.add(new Vector(3, 3)); v1.add(new Vector(1, 3));
        Polygon square1 = new Polygon(v1);

        List<Vector> v2 = new ArrayList<>();
        v2.add(new Vector(2.5, 1)); v2.add(new Vector(4.5, 1));
        v2.add(new Vector(4.5, 3)); v2.add(new Vector(2.5, 3));
        Polygon square2Colliding = new Polygon(v2);

        List<Vector> v3 = new ArrayList<>();
        v3.add(new Vector(5, 5)); v3.add(new Vector(7, 5));
        v3.add(new Vector(7, 7)); v3.add(new Vector(5, 7));
        Polygon square3Safe = new Polygon(v3);

        boolean p1 = SeparatingAxisTheorem.checkCollision(square1, square2Colliding);
        boolean p2 = !SeparatingAxisTheorem.checkCollision(square1, square3Safe);

        if (p1 && p2) {
            System.out.println("Java Separating Axis Theorem (SAT) Test Passed!");
        } else {
            System.exit(1);
        }
    }
}