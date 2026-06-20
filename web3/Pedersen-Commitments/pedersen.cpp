#include <iostream>
#include <random>
#include <cassert>

using namespace std;

class PedersenCommitment {
private:
    long long p = 2083;
    long long g = 2;
    long long h = 3;

    long long modPow(long long base, long long exp, long long mod) {
        long long res = 1;
        long long b = base % mod;
        long long e = exp;

        while (e > 0) {
            if (e % 2 == 1) res = (res * b) % mod;
            b = (b * b) % mod;
            e /= 2;
        }
        return res;
    }

public:
    long long generateBlindingFactor() {
        random_device rd;
        mt19937 gen(rd());
        uniform_int_distribution<long long> dis(1, p - 1);
        return dis(gen);
    }

    long long commit(long long value, long long blindingFactor) {
        long long cv = modPow(g, value, p);
        long long cr = modPow(h, blindingFactor, p);
        return (cv * cr) % p;
    }

    bool verify(long long commitment, long long value, long long blindingFactor) {
        long long expected = commit(value, blindingFactor);
        return expected == commitment;
    }

    long long homomorphicAdd(long long c1, long long c2) {
        return (c1 * c2) % p;
    }
};

// --- CI/CD Automated Test ---
int main() {
    PedersenCommitment crypto;

    long long aliceValue = 5;
    long long aliceBlinding = crypto.generateBlindingFactor();
    long long aliceCommitment = crypto.commit(aliceValue, aliceBlinding);

    long long bobValue = 10;
    long long bobBlinding = crypto.generateBlindingFactor();
    long long bobCommitment = crypto.commit(bobValue, bobBlinding);

    long long networkSumCommitment = crypto.homomorphicAdd(aliceCommitment, bobCommitment);

    long long combinedValue = aliceValue + bobValue;
    long long combinedBlinding = aliceBlinding + bobBlinding;

    assert(crypto.verify(networkSumCommitment, combinedValue, combinedBlinding) == true);
    assert(crypto.verify(networkSumCommitment, 999, combinedBlinding) == false);

    cout << "C++ Pedersen Commitment Test Passed! Homomorphic Confidential Transactions Verified.\n";
    return 0;
}