#include <iostream>
#include <cstdlib>
#include <ctime>
#include <cassert>

using namespace std;

class SchnorrZKP {
private:
    int p;
    int g;

    int modExp(int base, int exp) {
        int res = 1;
        base = base % p;
        while (exp > 0) {
            if (exp % 2 == 1) res = (res * base) % p;
            exp >>= 1;
            base = (base * base) % p;
        }
        return res;
    }

public:
    SchnorrZKP(int p_val, int g_val) : p(p_val), g(g_val) {
        srand(time(nullptr));
    }

    int generateKeys(int secretX) {
        return modExp(g, secretX);
    }

    bool proveAndVerify(int secretX, int publicY) {
        // Step 1: Commitment
        int k = (rand() % (p - 2)) + 1;
        int r = modExp(g, k);

        // Step 2: Challenge
        int c = (rand() % (p - 2)) + 1;

        // Step 3: Response
        int s = k + c * secretX;

        // Step 4: Verification
        int leftSide = modExp(g, s);
        int yC = modExp(publicY, c);
        int rightSide = (r * yC) % p;

        return leftSide == rightSide;
    }
};

// --- CI/CD Automated Test ---
int main() {
    int p = 23;
    int g = 5;
    SchnorrZKP zkp(p, g);

    int aliceSecret = 7;
    int alicePublic = zkp.generateKeys(aliceSecret);

    bool isVerified = zkp.proveAndVerify(aliceSecret, alicePublic);

    assert(isVerified == true);
    
    cout << "C++ Zero-Knowledge Proof Test Passed!\n";
    return 0;
}