#include <iostream>
#include <cmath>
#include <cassert>

using namespace std;

struct Vector3 {
    double x, y, z;
};

class Raymarcher {
private:
    const int MAX_STEPS = 100;
    const double MAX_DIST = 100.0;
    const double SURF_DIST = 0.01;

    double sdfSphere(Vector3 p, Vector3 center, double radius) {
        double dx = p.x - center.x;
        double dy = p.y - center.y;
        double dz = p.z - center.z;
        return sqrt(dx * dx + dy * dy + dz * dz) - radius;
    }

    double getDistance(Vector3 p) {
        return sdfSphere(p, {0.0, 0.0, 0.0}, 2.0);
    }

public:
    double raymarch(Vector3 ro, Vector3 rd) {
        double distOrigin = 0.0;

        for (int i = 0; i < MAX_STEPS; i++) {
            Vector3 p = {
                ro.x + rd.x * distOrigin,
                ro.y + rd.y * distOrigin,
                ro.z + rd.z * distOrigin
            };

            double distScene = getDistance(p);
            distOrigin += distScene;

            if (distScene < SURF_DIST || distOrigin > MAX_DIST) {
                break;
            }
        }
        return distOrigin;
    }
};

// --- CI/CD Automated Test ---
int main() {
    Raymarcher engine;
    Vector3 rayOrigin = {0.0, 0.0, -5.0};
    Vector3 rayDirection = {0.0, 0.0, 1.0};

    double hitDistance = engine.raymarch(rayOrigin, rayDirection);

    assert(abs(hitDistance - 3.0) < 0.05);
    
    cout << "C++ Raymarching SDF Test Passed! Hit distance: " << hitDistance << "\n";
    return 0;
}