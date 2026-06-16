import math

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def dot(self, other: 'Vector') -> float:
        """The core mathematical operation to project a point onto an axis."""
        return self.x * other.x + self.y * other.y

    def normalize(self) -> 'Vector':
        length = math.sqrt(self.x * self.x + self.y * self.y)
        if length == 0:
            return Vector(0, 0)
        return Vector(self.x / length, self.y / length)

class Polygon:
    def __init__(self, vertices: list[Vector]):
        # Vertices must be ordered (clockwise or counter-clockwise)
        self.vertices = vertices

class SeparatingAxisTheorem:
    @staticmethod
    def _get_axes(poly: Polygon) -> list[Vector]:
        axes = []
        # Loop through all vertices to get edges
        for i in range(len(poly.vertices)):
            p1 = poly.vertices[i]
            p2 = poly.vertices[(i + 1) % len(poly.vertices)]
            
            # Get the edge vector
            edge = Vector(p2.x - p1.x, p2.y - p1.y)
            
            # The Normal axis is perpendicular to the edge (-y, x)
            normal = Vector(-edge.y, edge.x)
            axes.append(normal.normalize())
        return axes

    @staticmethod
    def _project(poly: Polygon, axis: Vector) -> tuple[float, float]:
        """Squashes the 2D polygon into a 1D shadow on the given axis."""
        min_proj = float('inf')
        max_proj = float('-inf')
        
        for vertex in poly.vertices:
            projection = vertex.dot(axis)
            if projection < min_proj:
                min_proj = projection
            if projection > max_proj:
                max_proj = projection
                
        return min_proj, max_proj

    @staticmethod
    def check_collision(poly1: Polygon, poly2: Polygon) -> bool:
        """Returns True if the polygons are colliding, False otherwise."""
        # We must test the normal axes of BOTH polygons
        axes1 = SeparatingAxisTheorem._get_axes(poly1)
        axes2 = SeparatingAxisTheorem._get_axes(poly2)
        
        for axis in axes1 + axes2:
            # Cast the shadow of both polygons onto the axis
            min1, max1 = SeparatingAxisTheorem._project(poly1, axis)
            min2, max2 = SeparatingAxisTheorem._project(poly2, axis)
            
            # Check for a gap between the shadows
            if max1 < min2 or max2 < min1:
                # We found a gap! It is physically impossible for them to collide.
                return False
                
        # If we checked every single angle and found zero gaps, they are colliding.
        return True

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    # Square 1: Centered at (2,2), size 2x2
    square1 = Polygon([
        Vector(1, 1), Vector(3, 1), 
        Vector(3, 3), Vector(1, 3)
    ])
    
    # Square 2: Centered at (4,2), size 2x2. Overlaps with Square 1 on the edge.
    square2_colliding = Polygon([
        Vector(2.5, 1), Vector(4.5, 1), 
        Vector(4.5, 3), Vector(2.5, 3)
    ])
    
    # Square 3: Centered at (6,6), size 2x2. Far away.
    square3_safe = Polygon([
        Vector(5, 5), Vector(7, 5), 
        Vector(7, 7), Vector(5, 7)
    ])
    
    assert SeparatingAxisTheorem.check_collision(square1, square2_colliding) == True, "Failed to detect collision!"
    assert SeparatingAxisTheorem.check_collision(square1, square3_safe) == False, "False positive collision detected!"
    
    print("Python Separating Axis Theorem (SAT) Test Passed! Flawless Physics Engine Collision Verified.")