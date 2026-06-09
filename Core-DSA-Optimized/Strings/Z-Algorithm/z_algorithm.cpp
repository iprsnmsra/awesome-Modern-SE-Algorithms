#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cassert>

using namespace std;

class ZAlgorithm {
private:
    static vector<int> getZArray(const string& s) {
        int n = s.length();
        vector<int> z(n, 0);
        int L = 0, R = 0;

        for (int i = 1; i < n; i++) {
            if (i <= R) {
                z[i] = min(R - i + 1, z[i - L]);
            }

            while (i + z[i] < n && s[z[i]] == s[i + z[i]]) {
                z[i]++;
            }

            if (i + z[i] - 1 > R) {
                L = i;
                R = i + z[i] - 1;
            }
        }

        return z;
    }

public:
    static vector<int> search(const string& pattern, const string& text) {
        vector<int> matches;
        if (pattern.empty() || text.empty()) return matches;

        string concat = pattern + "$" + text;
        int m = pattern.length();
        vector<int> zArray = getZArray(concat);

        for (int i = 0; i < zArray.size(); i++) {
            if (zArray[i] == m) {
                matches.push_back(i - m - 1);
            }
        }

        return matches;
    }
};

// --- CI/CD Automated Test ---
int main() {
    string text = "AABAACAADAABAABA";
    string pattern = "AABA";

    vector<int> results = ZAlgorithm::search(pattern, text);

    assert(results.size() == 3);
    assert(results[0] == 0);
    assert(results[1] == 9);
    assert(results[2] == 12);

    cout << "C++ Z-Algorithm Pattern Matching Test Passed!\n";
    return 0;
}