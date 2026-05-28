using System;

public class Program {
    public class Vector3 {
        public double X, Y, Z;
        public Vector3(double x, double y, double z) { X = x; Y = y; Z = z; }
    }

    public class Raymarcher {
        private const int MaxSteps = 100;
        private const double MaxDist = 100.0;
        private const double SurfDist = 0.01;

        private double SdfSphere(Vector3 p, Vector3 center, double radius) {
            double dx = p.X - center.X;
            double dy = p.Y - center.Y;
            double dz = p.Z - center.Z;
            return Math.Sqrt(dx * dx + dy * dy + dz * dz) - radius;
        }

        private double GetDistance(Vector3 p) {
            return SdfSphere(p, new Vector3(0, 0, 0), 2.0);
        }

        public double Raymarch(Vector3 ro, Vector3 rd) {
            double distOrigin = 0.0;

            for (int i = 0; i < MaxSteps; i++) {
                var p = new Vector3(
                    ro.X + rd.X * distOrigin,
                    ro.Y + rd.Y * distOrigin,
                    ro.Z + rd.Z * distOrigin
                );

                double distScene = GetDistance(p);
                distOrigin += distScene;

                if (distScene < SurfDist || distOrigin > MaxDist) {
                    break;
                }
            }
            return distOrigin;
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var engine = new Raymarcher();
        var rayOrigin = new Vector3(0.0, 0.0, -5.0);
        var rayDirection = new Vector3(0.0, 0.0, 1.0);

        double hitDistance = engine.Raymarch(rayOrigin, rayDirection);

        if (Math.Abs(hitDistance - 3.0) < 0.05) {
            Console.WriteLine($"C# Raymarching SDF Test Passed! Hit distance: {hitDistance:F4}");
            return 0;
        }
        return 1;
    }
}