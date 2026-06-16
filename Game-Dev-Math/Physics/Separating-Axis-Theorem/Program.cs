using System;
using System.Collections.Generic;

public class Program {
    public class Vector {
        public double X { get; }
        public double Y { get; }

        public Vector(double x, double y) {
            X = x; Y = y;
        }

        public double Dot(Vector other) {
            return X * other.X + Y * other.Y;
        }

        public Vector Normalize() {
            double length = Math.Sqrt(X * X + Y * Y);
            if (length == 0) return new Vector(0, 0);
            return new Vector(X / length, Y / length);
        }
    }

    public class Polygon {
        public List<Vector> Vertices { get; }
        public Polygon(List<Vector> vertices) {
            Vertices = vertices;
        }
    }

    public class SeparatingAxisTheorem {
        private static List<Vector> GetAxes(Polygon poly) {
            var axes = new List<Vector>();
            int n = poly.Vertices.Count;
            for (int i = 0; i < n; i++) {
                Vector p1 = poly.Vertices[i];
                Vector p2 = poly.Vertices[(i + 1) % n];
                
                Vector edge = new Vector(p2.X - p1.X, p2.Y - p1.Y);
                Vector normal = new Vector(-edge.Y, edge.X);
                axes.Add(normal.Normalize());
            }
            return axes;
        }

        private static (double Min, double Max) Project(Polygon poly, Vector axis) {
            double min = double.PositiveInfinity;
            double max = double.NegativeInfinity;
            
            foreach (var vertex in poly.Vertices) {
                double projection = vertex.Dot(axis);
                if (projection < min) min = projection;
                if (projection > max) max = projection;
            }
            return (min, max);
        }

        public static bool CheckCollision(Polygon poly1, Polygon poly2) {
            var axes = new List<Vector>();
            axes.AddRange(GetAxes(poly1));
            axes.AddRange(GetAxes(poly2));
            
            foreach (var axis in axes) {
                var p1 = Project(poly1, axis);
                var p2 = Project(poly2, axis);
                
                if (p1.Max < p2.Min || p2.Max < p1.Min) {
                    return false; // Gap found
                }
            }
            return true;
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var square1 = new Polygon(new List<Vector> {
            new Vector(1, 1), new Vector(3, 1), new Vector(3, 3), new Vector(1, 3)
        });

        var square2Colliding = new Polygon(new List<Vector> {
            new Vector(2.5, 1), new Vector(4.5, 1), new Vector(4.5, 3), new Vector(2.5, 3)
        });

        var square3Safe = new Polygon(new List<Vector> {
            new Vector(5, 5), new Vector(7, 5), new Vector(7, 7), new Vector(5, 7)
        });

        bool p1 = SeparatingAxisTheorem.CheckCollision(square1, square2Colliding);
        bool p2 = !SeparatingAxisTheorem.CheckCollision(square1, square3Safe);

        if (p1 && p2) {
            Console.WriteLine("C# Separating Axis Theorem (SAT) Test Passed!");
            return 0;
        }
        return 1;
    }
}