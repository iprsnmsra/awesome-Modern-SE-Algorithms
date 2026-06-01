#include <iostream>
#include <string>
#include <vector>
#include <cassert>

using namespace std;

class Geohasher {
private:
    static constexpr const char* BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz";

public:
    static string encode(double lat, double lon, int precision = 12) {
        vector<double> latInterval = {-90.0, 90.0};
        vector<double> lonInterval = {-180.0, 180.0};
        
        string geohash = "";
        vector<int> bits = {16, 8, 4, 2, 1};
        
        int bit = 0;
        int ch = 0;
        bool evenBit = true;

        while (geohash.length() < precision) {
            if (evenBit) {
                double mid = (lonInterval[0] + lonInterval[1]) / 2;
                if (lon > mid) {
                    ch |= bits[bit];
                    lonInterval[0] = mid;
                } else {
                    lonInterval[1] = mid;
                }
            } else {
                double mid = (latInterval[0] + latInterval[1]) / 2;
                if (lat > mid) {
                    ch |= bits[bit];
                    latInterval[0] = mid;
                } else {
                    latInterval[1] = mid;
                }
            }

            evenBit = !evenBit;

            if (bit < 4) {
                bit++;
            } else {
                geohash += BASE32[ch];
                bit = 0;
                ch = 0;
            }
        }

        return geohash;
    }
};

// --- CI/CD Automated Test ---
int main() {
    double lat = 37.8199;
    double lon = -122.4783;
    
    string result = Geohasher::encode(lat, lon, 9);
    
    assert(result == "9q8zh4yvc");
    
    cout << "C++ Geohashing Test Passed! (Result: " << result << ")\n";
    return 0;
}