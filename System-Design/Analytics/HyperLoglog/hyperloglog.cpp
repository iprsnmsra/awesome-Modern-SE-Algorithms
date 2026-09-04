#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>
#include <cassert>

using namespace std;

class HyperLogLog {
private:
    int b;
    int m;
    vector<int> registers;
    double alpha;

    uint32_t fnv1a32(const string& data) {
        uint32_t h = 0x811c9dc5;
        for (char c : data) {
            h ^= static_cast<uint8_t>(c);
            h *= 0x01000193;
        }
        return h;
    }

public:
    HyperLogLog(int b = 8) : b(b) {
        m = 1 << b;
        registers.assign(m, 0);

        if (m == 16) alpha = 0.673;
        else if (m == 32) alpha = 0.697;
        else if (m == 64) alpha = 0.709;
        else alpha = 0.7213 / (1 + 1.079 / m);
    }

    void add(const string& item) {
        uint32_t h = fnv1a32(item);
        uint32_t index = h & (m - 1);
        uint32_t w = h >> b;

        int rank = 1;
        if (w == 0) {
            rank = 32 - b + 1;
        } else {
            while ((w & 1) == 0) {
                rank++;
                w >>= 1;
            }
        }

        registers[index] = max(registers[index], rank);
    }

    int estimate() {
        double Z = 0;
        int v = 0;

        for (int r : registers) {
            Z += pow(2.0, -r);
            if (r == 0) v++;
        }

        double E = (alpha * m * m) / Z;

        if (E <= 2.5 * m && v > 0) {
            E = m * log(static_cast<double>(m) / v);
        }

        return static_cast<int>(E);
    }
};

// --- CI/CD Automated Test ---
int main() {
    HyperLogLog hll(8);
    int exactCount = 10000;

    for (int i = 0; i < exactCount; i++) {
        hll.add("user_id_" + to_string(i));
    }

    int estimatedCount = hll.estimate();
    double errorPercentage = abs(static_cast<double>(exactCount) - estimatedCount) / exactCount * 100.0;

    cout << "Exact True Count: " << exactCount << "\n";
    cout << "HLL Estimation:   " << estimatedCount << "\n";
    cout << "Margin of Error:  " << errorPercentage << "%\n";

    assert(errorPercentage < 10.0);

    cout << "\nC++ HyperLogLog Test Passed! Big Data O(1) Memory Engine Verified.\n";
    return 0;
}