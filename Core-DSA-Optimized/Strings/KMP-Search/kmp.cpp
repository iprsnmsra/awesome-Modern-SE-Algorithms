#include <iostream>
#include <vector>
#include <string>
#include <cassert>

using namespace std;

class KMPSearch {
private:
    static vector<int> computeLPS(const string& pattern) {
        int m = pattern.length();
        vector<int> lps(m, 0);
        int len = 0;
        int i = 1;

        while (i < m) {
            if (pattern[i] == pattern[len]) {
                len++;
                lps[i] = len;
                i++;
            } else {
                if (len != 0) {
                    len = lps[len - 1];
                } else {
                    lps[i] = 0;
                    i++;
                }
            }
        }
        return lps;
    }

public:
    static vector<int> search(const string& text, const string& pattern) {
        vector<int> indices;
        int n = text.length();
        int m = pattern.length();
        if (m == 0) return indices;

        vector<int> lps = computeLPS(pattern);
        int i = 0;
        int j = 0;

        while (i < n) {
            if (pattern[j] == text[i]) {
                i++;
                j++;
            }
            if (j == m) {
                indices.push_back(i - j);
                j = lps[j - 1];
            } else if (i < n && pattern[j] != text[i]) {
                if (j != 0) {
                    j = lps[j - 1];
                } else {
                    i++;
                }
            }
        }
        return indices;
    }
};

// --- CI/CD Automated Test ---
int main() {
    string dnaSequence = "GACACCCTACACAACCACCACACACCCCCACACAC";
    string virusSignature = "ACAC";
    
    vector<int> matches = KMPSearch::search(dnaSequence, virusSignature);
    
    assert(matches.size() == 5);
    assert(matches[0] == 1);
    assert(matches[4] == 31);
    
    cout << "C++ KMP Search Test Passed!\n";
    return 0;
}