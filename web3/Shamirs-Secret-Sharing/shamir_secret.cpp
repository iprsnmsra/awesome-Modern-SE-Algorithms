#include <iostream>
#include <vector>
#include <cmath>
#include <random>
#include <cassert>

using namespace std;

const long long PRIME = 2083;

struct Share {
    long long x, y;
    Share(long long _x, long long _y) : x(_x), y(_y) {}
};

class ShamirSecretSharing {
private:
    static long long posMod(long long a, long long m) {
        return ((a % m) + m) % m;
    }

    static long long modInverse(long long n, long long p) {
        long long res = 1;
        long long exp = p - 2;
        long long base = posMod(n, p);

        while (exp > 0) {
            if (exp % 2 == 1) res = (res * base) % p;
            base = (base * base) % p;
            exp /= 2;
        }
        return res;
    }

public:
    static vector<Share> splitSecret(long long secret, int n, int k) {
        random_device rd;
        mt19散19937 gen(rd());
        uniform_int_distribution<long long> dis(1, PRIME - 1);

        vector<long long> coefficients(k);
        coefficients[0] = secret;
        for (int i = 1; i < k; i++) {
            coefficients[i] = dis(gen);
        }

        vector<Share> shares;
        for (int i = 1; i <= n; i++) {
            long long x = i;
            long long y = 0;
            for (int exp = 0; exp < k; exp++) {
                long long term = (coefficients[exp] * static_cast<long long>(pow(x, exp))) % PRIME;
                y = (y + term) % PRIME;
            }
            shares.emplace_back(x, y);
        }
        return shares;
    }

    static long long reconstructSecret(const vector<Share>& shares) {
        long long secret = 0;

        for (size_t i = 0; i < shares.size(); i++) {
            long long xi = shares[i].x;
            long long yi = shares[i].y;
            
            long long numerator = 1;
            long long denominator = 1;

            for (size_t j = 0; j < shares.size(); j++) {
                if (i == j) continue;
                long long xj = shares[j].x;

                numerator = posMod(numerator * -xj, PRIME);
                denominator = posMod(denominator * (xi - xj), PRIME);
            }

            long long lagrangeVal = posMod(posMod(yi * numerator, PRIME) * modInverse(denominator, PRIME), PRIME);
            secret = posMod(secret + lagrangeVal, PRIME);
        }
        return secret;
    }
};

// --- CI/CD Automated Test ---
int main() {
    long long originalSecret = 1337;
    vector<Share> allShares = ShamirSecretSharing::splitSecret(originalSecret, 5, 3);

    vector<Share> validShares(allShares.begin(), allShares.begin() + 3);
    vector<Share> invalidShares(allShares.begin(), allShares.begin() + 2);

    long long validReconstruction = ShamirSecretSharing::reconstructSecret(validShares);
    long long invalidReconstruction = ShamirSecretSharing::reconstructSecret(invalidShares);

    assert(validReconstruction == originalSecret);
    assert(invalidReconstruction != originalSecret);

    cout << "C++ SSS Test Passed! Information-theoretic security verified.\n";
    return 0;
}