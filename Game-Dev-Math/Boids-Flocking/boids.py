import math

class Boid:
    def __init__(self, x: float, y: float, vx: float, vy: float):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

class SwarmSimulation:
    def __init__(self, boids: list[Boid], visual_range: float = 50.0):
        self.boids = boids
        self.visual_range = visual_range

    def distance(self, b1: Boid, b2: Boid) -> float:
        return math.sqrt((b1.x - b2.x)**2 + (b1.y - b2.y)**2)

    def tick(self):
        # We calculate the new velocities for all boids before applying them
        # so they don't affect each other mid-calculation.
        new_velocities = []

        for boid in self.boids:
            cx, cy = 0.0, 0.0 # Cohesion center
            vx_avg, vy_avg = 0.0, 0.0 # Alignment velocity
            sx, sy = 0.0, 0.0 # Separation vector
            neighbors = 0

            for other in self.boids:
                if boid == other: continue
                
                dist = self.distance(boid, other)
                if dist < self.visual_range:
                    # 1. Cohesion (accumulate positions)
                    cx += other.x
                    cy += other.y
                    
                    # 2. Alignment (accumulate velocities)
                    vx_avg += other.vx
                    vy_avg += other.vy
                    
                    # 3. Separation (steer away if too close)
                    if dist < 20.0: # Minimum personal space
                        sx += boid.x - other.x
                        sy += boid.y - other.y
                        
                    neighbors += 1

            if neighbors > 0:
                cx /= neighbors
                cy /= neighbors
                vx_avg /= neighbors
                vy_avg /= neighbors

                # Apply rule weights (these decimal values tune the swarm's behavior)
                new_vx = boid.vx + (cx - boid.x) * 0.01 + (vx_avg - boid.vx) * 0.05 + sx * 0.1
                new_vy = boid.vy + (cy - boid.y) * 0.01 + (vy_avg - boid.vy) * 0.05 + sy * 0.1
            else:
                new_vx, new_vy = boid.vx, boid.vy

            new_velocities.append((new_vx, new_vy))

        # Apply physics to positions
        for i, boid in enumerate(self.boids):
            boid.vx, boid.vy = new_velocities[i]
            boid.x += boid.vx
            boid.y += boid.vy

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    # Create 3 boids close to each other
    flock = [
        Boid(0.0, 0.0, 1.0, 0.0),
        Boid(5.0, 5.0, 0.0, 1.0),
        Boid(-5.0, 5.0, -1.0, 1.0)
    ]
    
    sim = SwarmSimulation(flock)
    
    # Store initial position of Boid 1
    initial_x = flock[0].x
    
    # Run the physics engine for 1 frame
    sim.tick()
    
    # Verify the swarm math caused the boid to move
    assert flock[0].x != initial_x, "Boid physics engine failed to update!"
    
    print("Python Boids Swarm Intelligence Test Passed!")