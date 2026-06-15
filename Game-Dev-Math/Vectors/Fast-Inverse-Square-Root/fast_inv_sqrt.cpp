#include <iostream>
#include <cmath>
#include <cstring>
#include <cstdint>
#include <cassert>

using namespace std;

class FastMath {
public:
    static float fastInvSqrt(float number) {
        float threehalfs = 1.5F;
        float x2 = number * 0.5F;
        float y = number;
        uint32_t i;
        
        // Principal Engineer Rule: Use memcpy to avoid Strict Aliasing UB!
        // The compiler will optimize this memcpy completely out of existence.
        memcpy(&i, &y, sizeof(i));
        
        i = 0x5f3759df - (i >> 1);
        
        memcpy(&y, &i, sizeof(y));
        
        // 1st iteration of Newton's Method
        y = y * (threehalfs - (x2 * y * y));
        
        return y;
    }
};

// --- CI/CD Automated Test ---
int main() {
    float testVal = 25.0F;
    
    float standardResult = 1.0F / sqrt(testVal);
    float fastResult = FastMath::fastInvSqrt(testVal);
    
    float errorMargin = abs(standardResult - fastResult);
    
    cout << "Standard Math: " << standardResult << "\n";
    cout << "Fast Inv Sqrt: " << fastResult << "\n";
    cout << "Error Margin:  " << errorMargin << "\n";
    
    assert(errorMargin < 0.01);
    
    cout << "\nC++ Fast Inverse Square Root Test Passed! (Hardware Hacker Mode Verified)\n";
    return 0;
}