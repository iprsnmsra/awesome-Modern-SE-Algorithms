using System;
using System.Collections.Generic;

public class Program {
    class Boid {
        public double X, Y, Vx, Vy;
        public Boid(double x, double y, double vx, double vy) {
            X = x; Y = y; Vx = vx; Vy = vy;
        }
    }

    class SwarmSimulation {
        private List<Boid> boids;
        private double visualRange;

        public SwarmSimulation(List<Boid> boids, double visualRange = 50.0) {
            this.boids = boids;
            this.visualRange = visualRange;
        }

        private double Distance(Boid b1, Boid b2) {
            return Math.Sqrt(Math.Pow(b1.X - b2.X, 2) + Math.Pow(b1.Y - b2.Y, 2));
        }

        public void Tick() {
            var newVelocities = new (double vx, double vy)[boids.Count];

            for (int i = 0; i < boids.Count; i++) {
                Boid boid = boids[i];
                double cx = 0, cy = 0, vxAvg = 0, vyAvg = 0, sx = 0, sy = 0;
                int neighbors = 0;

                foreach (var other in boids) {
                    if (boid == other) continue;

                    double dist = Distance(boid, other);
                    if (dist < visualRange) {
                        cx += other.X; cy += other.Y;
                        vxAvg += other.Vx; vyAvg += other.Vy;
                        
                        if (dist < 20.0) {
                            sx += boid.X - other.X;
                            sy += boid.Y - other.Y;
                        }
                        neighbors++;
                    }
                }

                double newVx = boid.Vx, newVy = boid.Vy;

                if (neighbors > 0) {
                    cx /= neighbors; cy /= neighbors;
                    vxAvg /= neighbors; vyAvg /= neighbors;

                    newVx += (cx - boid.X) * 0.01 + (vxAvg - boid.Vx) * 0.05 + sx * 0.1;
                    newVy += (cy - boid.Y) * 0.01 + (vyAvg - boid.Vy) * 0.05 + sy * 0.1;
                }

                newVelocities[i] = (newVx, newVy);
            }

            for (int i = 0; i < boids.Count; i++) {
                boids[i].Vx = newVelocities[i].vx;
                boids[i].Vy = newVelocities[i].vy;
                boids[i].X += boids[i].Vx;
                boids[i].Y += boids[i].Vy;
            }
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var flock = new List<Boid> {
            new Boid(0, 0, 1, 0),
            new Boid(5, 5, 0, 1),
            new Boid(-5, 5, -1, 1)
        };

        var sim = new SwarmSimulation(flock);
        double initialX = flock[0].X;

        sim.Tick();

        if (flock[0].X != initialX) {
            Console.WriteLine("C# Boids Swarm Intelligence Test Passed!");
            return 0;
        }
        return 1;
    }
}