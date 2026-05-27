#include <iostream>
#include <vector>
#include <memory>
#include <cassert>

using namespace std;

struct Point {
    double x, y;
};

struct Rectangle {
    double x, y, w, h;

    bool contains(const Point& p) const {
        return (p.x >= x - w && p.x <= x + w && p.y >= y - h && p.y <= y + h);
    }

    bool intersects(const Rectangle& range) const {
        return !(range.x - range.w > x + w || range.x + range.w < x - w ||
                 range.y - range.h > y + h || range.y + range.h < y - h);
    }
};

class QuadTree {
private:
    Rectangle boundary;
    int capacity;
    vector<Point> points;
    bool divided;
    
    unique_ptr<QuadTree> nw, ne, sw, se;

    void subdivide() {
        double x = boundary.x, y = boundary.y, w = boundary.w, h = boundary.h;
        ne = make_unique<QuadTree>(Rectangle{x + w/2, y - h/2, w/2, h/2}, capacity);
        nw = make_unique<QuadTree>(Rectangle{x - w/2, y - h/2, w/2, h/2}, capacity);
        se = make_unique<QuadTree>(Rectangle{x + w/2, y + h/2, w/2, h/2}, capacity);
        sw = make_unique<QuadTree>(Rectangle{x - w/2, y + h/2, w/2, h/2}, capacity);
        divided = true;
    }

public:
    QuadTree(Rectangle b, int c) : boundary(b), capacity(c), divided(false) {}

    bool insert(Point p) {
        if (!boundary.contains(p)) return false;

        if (points.size() < capacity) {
            points.push_back(p);
            return true;
        }

        if (!divided) subdivide();

        if (ne->insert(p)) return true;
        if (nw->insert(p)) return true;
        if (se->insert(p)) return true;
        if (sw->insert(p)) return true;

        return false;
    }

    void query(const Rectangle& range, vector<Point>& found) {
        if (!boundary.intersects(range)) return;

        for (const auto& p : points) {
            if (range.contains(p)) found.push_back(p);
        }

        if (divided) {
            nw->query(range, found);
            ne->query(range, found);
            sw->query(range, found);
            se->query(range, found);
        }
    }
};

// --- CI/CD Automated Test ---
int main() {
    Rectangle boundary = {100, 100, 100, 100};
    QuadTree qt(boundary, 4);

    qt.insert({50, 50});
    qt.insert({60, 60});
    qt.insert({40, 40});
    qt.insert({45, 45});
    qt.insert({150, 150});

    Rectangle queryBox = {50, 50, 20, 20};
    vector<Point> results;
    qt.query(queryBox, results);

    bool hasDistant = false;
    for (const auto& p : results) {
        if (p.x == 150) hasDistant = true;
    }

    assert(results.size() == 4);
    assert(!hasDistant);
    
    cout << "C++ QuadTree Spatial Partitioning Test Passed!\n";
    return 0;
}