export class FastMath {
    public static fastInvSqrt(number: number): number {
        // We use an ArrayBuffer to share the exact same physical memory block 
        // between a Float array and an Integer array. This is the JS equivalent of C-pointers.
        const buffer = new ArrayBuffer(4);
        const floatView = new Float32Array(buffer);
        const intView = new Int32Array(buffer);

        const threehalfs = 1.5;
        const x2 = number * 0.5;
        
        floatView[0] = number;
        
        // Evil floating point bit level hacking
        intView[0] = 0x5f3759df - (intView[0] >> 1);
        
        let y = floatView[0];
        
        // 1st iteration of Newton's Method
        y = y * (threehalfs - (x2 * y * y));
        
        return y;
    }
}

// --- CI/CD Automated Test ---
const testVal = 25.0;
const standardResult = 1.0 / Math.sqrt(testVal);
const fastResult = FastMath.fastInvSqrt(testVal);

const errorMargin = Math.abs(standardResult - fastResult);

console.log(`Standard Math: ${standardResult}`);
console.log(`Fast Inv Sqrt: ${fastResult}`);
console.log(`Error Margin:  ${errorMargin.toFixed(6)}`);

if (errorMargin < 0.01) {
    console.log("\nTypeScript Fast Inverse Square Root Test Passed! (Hardware Hacker Mode Verified)");
} else {
    process.exit(1);
}