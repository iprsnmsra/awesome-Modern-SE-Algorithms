import math

class Raymarcher:
    def __init__(self, max_steps=100, max_dist=100.0, surf_dist=0.01):
        self.max_steps = max_steps
        self.max_dist = max_dist
        self.surf_dist = surf_dist

    def sdf_sphere(self, p: tuple, center: tuple, radius: float) -> float:
        # Distance from a point 'p' to the surface of a sphere
        dx = p[0] - center[0]
        dy = p[1] - center[1]
        dz = p[2] - center[2]
        return math.sqrt(dx*dx + dy*dy + dz*dz) - radius

    def get_distance(self, p: tuple) -> float:
        # Define the scene: A single sphere at the origin (0,0,0) with radius 2
        return self.sdf_sphere(p, (0.0, 0.0, 0.0), 2.0)

    def raymarch(self, ro: tuple, rd: tuple) -> float:
        # ro = Ray Origin, rd = Ray Direction (normalized)
        dist_origin = 0.0
        
        for _ in range(self.max_steps):
            # Calculate current position along the ray
            p = (
                ro[0] + rd[0] * dist_origin, 
                ro[1] + rd[1] * dist_origin, 
                ro[2] + rd[2] * dist_origin
            )
            
            # Ask the SDF how far away the closest object is
            dist_scene = self.get_distance(p)
            
            # Safely march forward by that exact distance
            dist_origin += dist_scene
            
            # Check for a "hit" or "out of bounds"
            if dist_scene < self.surf_dist or dist_origin > self.max_dist:
                break
                
        return dist_origin

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    engine = Raymarcher()
    
    # Camera is 5 units back on the Z axis
    ray_origin = (0.0, 0.0, -5.0)
    
    # Looking perfectly forward along the Z axis
    ray_direction = (0.0, 0.0, 1.0) 
    
    # Fire the ray!
    hit_distance = engine.raymarch(ray_origin, ray_direction)
    
    # The sphere is at Z=0 with radius 2. Its front surface is at Z=-2.
    # Therefore, the ray traveling from Z=-5 should hit the surface after exactly 3.0 units.
    assert abs(hit_distance - 3.0) < 0.05, f"Raymarching math failed! Expected ~3.0, got {hit_distance}"
    
    print(f"Python Raymarching SDF Test Passed! Hit surface at distance: {hit_distance:.4f}")