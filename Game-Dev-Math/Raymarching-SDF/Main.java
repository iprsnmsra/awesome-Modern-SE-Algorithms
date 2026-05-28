public class Main {
    static class Vector3 {
        double x, y, z;
        public Vector3(double x, double y, double z) {
            this.x = x; this.y = y; this.z = z;
        }
    }

    static class Raymarcher {
        private final int MAX_STEPS = 100;
        private final double MAX_DIST = 100.0;
        private final double SURF_DIST = 0.01;

        private double sdfSphere(Vector3 p, Vector3 center, double radius) {
            double dx = p.x - center.x;
            double dy = p.y - center.y;
            double dz = p.z - center.z;
            return Math.sqrt(dx * dx + dy * dy + dz * dz) - radius;
        }

        private double getDistance(Vector3 p) {
            return sdfSphere(p, new Vector3(0, 0, 0), 2.0);
        }

        public double raymarch(Vector3 ro, Vector3 rd) {
            double distOrigin = 0.0;

            for (int i = 0; i < MAX_STEPS; i++) {
                Vector3 p = new Vector3(
                    ro.x + rd.x * distOrigin,
                    ro.y + rd.y * distOrigin,
                    ro.z + rd.z * distOrigin
                );

                double distScene = getDistance(p);
                distOrigin += distScene;

                if (distScene < SURF_DIST || distOrigin > MAX_DIST) {
                    break;
                }
            }
            return distOrigin;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        Raymarcher engine = new Raymarcher();
        Vector3 rayOrigin = new Vector3(0.0, 0.0, -5.0);
        Vector3 rayDirection = new Vector3(0.0, 0.0, 1.0);

        double hitDistance = engine.raymarch(rayOrigin, rayDirection);

        if (Math.abs(hitDistance - 3.0) < 0.05) {
            System.out.printf("Java Raymarching SDF Test Passed! Hit distance: %.4f\n", hitDistance);
        } else {
            System.exit(1);
        }
    }
}