export class SHA256 {
    private static readonly K: number[] = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ];

    private static rotr(x: number, n: number): number {
        return (x >>> n) | (x << (32 - n));
    }

    public static hash(message: string): string {
        const h = [
            0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
            0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
        ];

        // String to UTF-8 Bytes
        const msgBytes: number[] = [];
        for (let i = 0; i < message.length; i++) {
            msgBytes.push(message.charCodeAt(i));
        }

        const ml = msgBytes.length * 8;
        msgBytes.push(0x80);
        while ((msgBytes.length * 8) % 512 !== 448) {
            msgBytes.push(0x00);
        }

        // Append 64-bit length (Big Endian)
        for (let i = 7; i >= 0; i--) {
            msgBytes.push((ml >>> (i * 8)) & 0xFF);
        }

        for (let i = 0; i < msgBytes.length; i += 64) {
            const w: number[] = new Array(64).fill(0);
            for (let j = 0; j < 16; j++) {
                w[j] = (msgBytes[i + j * 4] << 24) | (msgBytes[i + j * 4 + 1] << 16) |
                       (msgBytes[i + j * 4 + 2] << 8) | (msgBytes[i + j * 4 + 3]);
                w[j] >>>= 0; // Force unsigned 32-bit
            }

            for (let j = 16; j < 64; j++) {
                const s0 = this.rotr(w[j - 15], 7) ^ this.rotr(w[j - 15], 18) ^ (w[j - 15] >>> 3);
                const s1 = this.rotr(w[j - 2], 17) ^ this.rotr(w[j - 2], 19) ^ (w[j - 2] >>> 10);
                w[j] = (w[j - 16] + s0 + w[j - 7] + s1) >>> 0;
            }

            let [a, b, c, d, e, f, g, hh] = h;

            for (let j = 0; j < 64; j++) {
                const S1 = this.rotr(e, 6) ^ this.rotr(e, 11) ^ this.rotr(e, 25);
                const ch = (e & f) ^ (~e & g);
                const temp1 = (hh + S1 + ch + this.K[j] + w[j]) >>> 0;

                const S0 = this.rotr(a, 2) ^ this.rotr(a, 13) ^ this.rotr(a, 22);
                const maj = (a & b) ^ (a & c) ^ (b & c);
                const temp2 = (S0 + maj) >>> 0;

                hh = g;
                g = f;
                f = e;
                e = (d + temp1) >>> 0;
                d = c;
                c = b;
                b = a;
                a = (temp1 + temp2) >>> 0;
            }

            h[0] = (h[0] + a) >>> 0;
            h[1] = (h[1] + b) >>> 0;
            h[2] = (h[2] + c) >>> 0;
            h[3] = (h[3] + d) >>> 0;
            h[4] = (h[4] + e) >>> 0;
            h[5] = (h[5] + f) >>> 0;
            h[6] = (h[6] + g) >>> 0;
            h[7] = (h[7] + hh) >>> 0;
        }

        return h.map(val => val.toString(16).padStart(8, '0')).join('');
    }
}

// --- CI/CD Automated Test ---
const testString = "hello world";
const customHash = SHA256.hash(testString);
const expectedHash = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9";

if (customHash === expectedHash) {
    console.log("TypeScript SHA-256 Engine Test Passed! Mathematical Bit-Scrambling Verified.");
} else {
    process.exit(1);
}