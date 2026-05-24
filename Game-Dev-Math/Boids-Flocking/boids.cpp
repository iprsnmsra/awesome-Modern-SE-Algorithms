#include <iostream>
#include <vector>
#include <cmath>
#include <cassert>

using namespace std;

struct Boid {
    double x, y, vx, vy;
};

class SwarmSimulation {
private:
    vector<Boid>& boids;
    double visualRange;

    double distance(const Boid& b1, const Boid& b2) {
        return sqrt(pow(b1.x - b2.x, 2) + pow(b1.y - b2.y, 2));
    }

public:
    SwarmSimulation(vector<Boid>& b, double range = 50.0) : boids(b), visualRange(range) {}

    void tick() {
        vector<pair<double, double>> newVelocities(boids.size());

        for (size_t i = 0; i < boids.size(); i++) {
            double cx = 0, cy = 0, vxAvg = 0, vyAvg = 0, sx = 0, sy = 0;
            int neighbors = 0;

            for (size_t j = 0; j < boids.size(); j++) {
                if (i == j) continue;

                double dist = distance(boids[i], boids[j]);
                if (dist < visualRange) {
                    cx += boids[j].x; cy += boids[j].y;
                    vxAvg += boids[j].vx; vyAvg += boids[j].vy;
                    
                    if (dist < 20.0) {
                        sx += boids[i].x - boids[j].x;
                        sy += boids[i].y - boids[j].y;
                    }
                    neighbors++;
                }
            }

            double newVx = boids[i].vx;
            double newVy = boids[i].vy;

            if (neighbors > 0) {
                cx /= neighbors; cy /= neighbors;
                vxAvg /= neighbors; vyAvg /= neighbors;

                newVx += (cx - boids[i].x) * 0.01 + (vxAvg - boids[i].vx) * 0.05 + sx * 0.1;
                newVy += (cy - boids[i].y) * 0.01 + (vyAvg - boids[i].vy) * 0.05 + sy * 0.1;
            }

            newVelocities[i] = {newVx, newVy};
        }

        for (size_t i = 0; i < boids.size(); i++) {
            boids[i].vx = newVelocities[i].first;
            boids[i].vy = newVelocities[i].second;
            boids[i].x += boids[i].vx;
            boids[i].y += boids[i].vy;
        }
    }
};

// --- CI/CD Automated Test ---
int main() {
    vector<Boid> flock = {
        {0.0, 0.0, 1.0, 0.0},
        {5.0, 5.0, 0.0, 1.0},
        {-5.0, 5.0, -1.0, 1.0}
    };

    SwarmSimulation sim(flock);
    double initialX = flock[0].x;

    sim.tick();

    assert(flock[0].x != initialX);
    cout << "C++ Boids Swarm Intelligence Test Passed!\n";
    return 0;
}