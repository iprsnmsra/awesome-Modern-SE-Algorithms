using System;
using System.Collections.Generic;
using System.Linq;

public class Program {
    public class Point {
        public double X, Y;
        public Point(double x, double y) { X = x; Y = y; }
    }

    public class Rectangle {
        public double X, Y, W, H;
        public Rectangle(double x, double y, double w, double h) {
            X = x; Y = y; W = w; H = h;
        }
        public bool Contains(Point p) {
            return (p.X >= X - W && p.X <= X + W && p.Y >= Y - H && p.Y <= Y + H);
        }
        public bool Intersects(Rectangle range) {
            return !(range.X - range.W > X + W || range.X + range.W < X - W ||
                     range.Y - range.H > Y + H || range.Y + range.H < Y - H);
        }
    }

    public class QuadTree {
        private Rectangle boundary;
        private int capacity;
        private List<Point> points;
        private bool divided = false;
        private QuadTree nw, ne, sw, se;

        public QuadTree(Rectangle boundary, int capacity) {
            this.boundary = boundary;
            this.capacity = capacity;
            this.points = new List<Point>();
        }

        private void Subdivide() {
            double x = boundary.X, y = boundary.Y, w = boundary.W, h = boundary.H;
            ne = new QuadTree(new Rectangle(x + w/2, y - h/2, w/2, h/2), capacity);
            nw = new QuadTree(new Rectangle(x - w/2, y - h/2, w/2, h/2), capacity);
            se = new QuadTree(new Rectangle(x + w/2, y + h/2, w/2, h/2), capacity);
            sw = new QuadTree(new Rectangle(x - w/2, y + h/2, w/2, h/2), capacity);
            divided = true;
        }

        public bool Insert(Point p) {
            if (!boundary.Contains(p)) return false;

            if (points.Count < capacity) {
                points.Add(p);
                return true;
            }
            if (!divided) Subdivide();
            
            if (ne.Insert(p)) return true;
            if (nw.Insert(p)) return true;
            if (se.Insert(p)) return true;
            if (sw.Insert(p)) return true;
            
            return false;
        }

        public List<Point> Query(Rectangle range, List<Point> found = null) {
            if (found == null) found = new List<Point>();
            if (!boundary.Intersects(range)) return found;

            foreach (var p in points) {
                if (range.Contains(p)) found.Add(p);
            }

            if (divided) {
                nw.Query(range, found);
                ne.Query(range, found);
                sw.Query(range, found);
                se.Query(range, found);
            }
            return found;
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var boundary = new Rectangle(100, 100, 100, 100);
        var qt = new QuadTree(boundary, 4);

        qt.Insert(new Point(50, 50));
        qt.Insert(new Point(60, 60));
        qt.Insert(new Point(40, 40));
        qt.Insert(new Point(45, 45));
        qt.Insert(new Point(150, 150));

        var queryBox = new Rectangle(50, 50, 20, 20);
        var results = qt.Query(queryBox);

        if (results.Count == 4 && !results.Any(p => p.X == 150)) {
            Console.WriteLine("C# QuadTree Spatial Partitioning Test Passed!");
            return 0;
        }
        return 1;
    }
}