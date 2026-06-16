#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <limits>
#include <cassert>

using namespace std;

struct Vector {
    double x, y;
    
    Vector(double _x, double _y) : x(_x), y(_y) {}
    
    double dot(const Vector& other) const {
        return x * other.x + y * other.y;
    }
    
    Vector normalize() const {
        double length = sqrt(x * x + y * y);
        if (length == 0) return Vector(0, 0);
        return Vector(x / length, y / length);
    }
};

struct Polygon {
    vector<Vector> vertices;
    Polygon(vector<Vector> v) : vertices(v) {}
};

class SeparatingAxisTheorem {
private:
    static vector<Vector> getAxes(const Polygon& poly) {
        vector<Vector> axes;
        int n = poly.vertices.size();
        for (int i = 0; i < n; i++) {
            Vector p1 = poly.vertices[i];
            Vector p2 = poly.vertices[(i + 1) % n];
            
            Vector edge(p2.x - p1.x, p2.y - p1.y);
            Vector normal(-edge.y, edge.x);
            axes.push_back(normal.normalize());
        }
        return axes;
    }

    static pair<double, double> project(const Polygon& poly, const Vector& axis) {
        double min_proj = numeric_limits<double>::infinity();
        double max_proj = -numeric_limits<double>::infinity();
        
        for (const auto& vertex : poly.vertices) {
            double projection = vertex.dot(axis);
            min_proj = min(min_proj, projection);
            max_proj = max(max_proj, projection);
        }
        return {min_proj, max_proj};
    }

public:
    static bool checkCollision(const Polygon& poly1, const Polygon& poly2) {
        vector<Vector> axes = getAxes(poly1);
        vector<Vector> axes2 = getAxes(poly2);
        axes.insert(axes.end(), axes2.begin(), axes2.end());
        
        for (const auto& axis : axes) {
            pair<double, double> p1 = project(poly1, axis);
            pair<double, double> p2 = project(poly2, axis);
            
            if (p1.second < p2.first || p2.second < p1.first) {
                return false; // Gap found, no collision
            }
        }
        return true;
    }
};

// --- CI/CD Automated Test ---
int main() {
    Polygon square1({{1, 1}, {3, 1}, {3, 3}, {1, 3}});
    Polygon square2Colliding({{2.5, 1}, {4.5, 1}, {4.5, 3}, {2.5, 3}});
    Polygon square3Safe({{5, 5}, {7, 5}, {7, 7}, {5, 7}});

    assert(SeparatingAxisTheorem::checkCollision(square1, square2Colliding) == true);
    assert(SeparatingAxisTheorem::checkCollision(square1, square3Safe) == false);

    cout << "C++ Separating Axis Theorem (SAT) Test Passed! Flawless Physics Engine Collision Verified.\n";
    return 0;
}