class Point:
    def __init__(self, x: float, y: float, user_data=None):
        self.x = x
        self.y = y
        self.user_data = user_data

class Rectangle:
    def __init__(self, x: float, y: float, w: float, h: float):
        # x, y is the center of the rectangle. w, h are the half-widths (distance from center to edge)
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def contains(self, point: Point) -> bool:
        return (self.x - self.w <= point.x <= self.x + self.w and
                self.y - self.h <= point.y <= self.y + self.h)

    def intersects(self, range_rect) -> bool:
        return not (range_rect.x - range_rect.w > self.x + self.w or
                    range_rect.x + range_rect.w < self.x - self.w or
                    range_rect.y - range_rect.h > self.y + self.h or
                    range_rect.y + range_rect.h < self.y - self.h)

class QuadTree:
    def __init__(self, boundary: Rectangle, capacity: int):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False

    def subdivide(self):
        x, y, w, h = self.boundary.x, self.boundary.y, self.boundary.w, self.boundary.h
        
        ne = Rectangle(x + w/2, y - h/2, w/2, h/2)
        nw = Rectangle(x - w/2, y - h/2, w/2, h/2)
        se = Rectangle(x + w/2, y + h/2, w/2, h/2)
        sw = Rectangle(x - w/2, y + h/2, w/2, h/2)
        
        self.northeast = QuadTree(ne, self.capacity)
        self.northwest = QuadTree(nw, self.capacity)
        self.southeast = QuadTree(se, self.capacity)
        self.southwest = QuadTree(sw, self.capacity)
        
        self.divided = True

    def insert(self, point: Point) -> bool:
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()

            if self.northeast.insert(point): return True
            if self.northwest.insert(point): return True
            if self.southeast.insert(point): return True
            if self.southwest.insert(point): return True

    def query(self, range_rect: Rectangle, found: list = None) -> list:
        if found is None:
            found = []

        if not self.boundary.intersects(range_rect):
            return found

        for p in self.points:
            if range_rect.contains(p):
                found.append(p)

        if self.divided:
            self.northwest.query(range_rect, found)
            self.northeast.query(range_rect, found)
            self.southwest.query(range_rect, found)
            self.southeast.query(range_rect, found)

        return found

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    # Create a 200x200 map centered at (100, 100)
    boundary = Rectangle(100, 100, 100, 100)
    qt = QuadTree(boundary, capacity=4)
    
    # Insert 5 points. The 5th point will force a subdivision!
    qt.insert(Point(50, 50))
    qt.insert(Point(60, 60))
    qt.insert(Point(40, 40))
    qt.insert(Point(45, 45))
    qt.insert(Point(150, 150)) # Triggers split
    
    # Query a small 40x40 box centered at (50, 50)
    query_box = Rectangle(50, 50, 20, 20)
    results = qt.query(query_box)
    
    assert len(results) == 4, f"Expected 4 points in query box, found {len(results)}"
    
    # Verify the distant point wasn't included
    for p in results:
        assert p.x != 150, "QuadTree math failed, included a point outside the query box!"
        
    print("Python QuadTree Spatial Partitioning Test Passed!")