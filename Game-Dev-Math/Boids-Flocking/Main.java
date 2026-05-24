import java.util.ArrayList;
import java.util.List;

public class Main {
    static class Boid {
        double x, y, vx, vy;
        public Boid(double x, double y, double vx, double vy) {
            this.x = x; this.y = y; this.vx = vx; this.vy = vy;
        }
    }

    static class SwarmSimulation {
        List<Boid> boids;
        double visualRange;

        public SwarmSimulation(List<Boid> boids, double visualRange) {
            this.boids = boids;
            this.visualRange = visualRange;
        }

        private double distance(Boid b1, Boid b2) {
            return Math.sqrt(Math.pow(b1.x - b2.x, 2) + Math.pow(b1.y - b2.y, 2));
        }

        public void tick() {
            double[][] newVelocities = new double[boids.size()][2];

            for (int i = 0; i < boids.size(); i++) {
                Boid boid = boids.get(i);
                double cx = 0, cy = 0, vxAvg = 0, vyAvg = 0, sx = 0, sy = 0;
                int neighbors = 0;

                for (Boid other : boids) {
                    if (boid == other) continue;

                    double dist = distance(boid, other);
                    if (dist < visualRange) {
                        cx += other.x; cy += other.y;
                        vxAvg += other.vx; vyAvg += other.vy;
                        
                        if (dist < 20.0) {
                            sx += boid.x - other.x;
                            sy += boid.y - other.y;
                        }
                        neighbors++;
                    }
                }

                double newVx = boid.vx;
                double newVy = boid.vy;

                if (neighbors > 0) {
                    cx /= neighbors; cy /= neighbors;
                    vxAvg /= neighbors; vyAvg /= neighbors;

                    newVx += (cx - boid.x) * 0.01 + (vxAvg - boid.vx) * 0.05 + sx * 0.1;
                    newVy += (cy - boid.y) * 0.01 + (vyAvg - boid.vy) * 0.05 + sy * 0.1;
                }

                newVelocities[i][0] = newVx;
                newVelocities[i][1] = newVy;
            }

            for (int i = 0; i < boids.size(); i++) {
                boids.get(i).vx = newVelocities[i][0];
                boids.get(i).vy = newVelocities[i][1];
                boids.get(i).x += boids.get(i).vx;
                boids.get(i).y += boids.get(i).vy;
            }
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        List<Boid> flock = new ArrayList<>();
        flock.add(new Boid(0, 0, 1, 0));
        flock.add(new Boid(5, 5, 0, 1));
        flock.add(new Boid(-5, 5, -1, 1));

        SwarmSimulation sim = new SwarmSimulation(flock, 50.0);
        double initialX = flock.get(0).x;

        sim.tick();

        if (flock.get(0).x != initialX) {
            System.out.println("Java Boids Swarm Intelligence Test Passed!");
        } else {
            System.exit(1);
        }
    }
}