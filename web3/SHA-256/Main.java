public class Main {
    static class SHA256 {
        private static final int[] K = {
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        };

        private static int rotr(int x, int n) {
            return (x >>> n) | (x << (32 - n));
        }

        public static String hash(byte[] message) {
            int[] h = {
                0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
                0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
            };

            int msgLen = message.length;
            long bitLen = (long) msgLen * 8;
            
            // Calculate padding size
            int padLen = 1;
            while ((msgLen + padLen + 8) % 64 != 0) {
                padLen++;
            }

            byte[] paddedMsg = new byte[msgLen + padLen + 8];
            System.arraycopy(message, 0, paddedMsg, 0, msgLen);
            paddedMsg[msgLen] = (byte) 0x80;

            for (int i = 0; i < 8; i++) {
                paddedMsg[paddedMsg.length - 1 - i] = (byte) (bitLen >>> (i * 8));
            }

            for (int i = 0; i < paddedMsg.length; i += 64) {
                int[] w = new int[64];
                for (int j = 0; j < 16; j++) {
                    w[j] = ((paddedMsg[i + j * 4] & 0xFF) << 24) |
                           ((paddedMsg[i + j * 4 + 1] & 0xFF) << 16) |
                           ((paddedMsg[i + j * 4 + 2] & 0xFF) << 8) |
                           (paddedMsg[i + j * 4 + 3] & 0xFF);
                }

                for (int j = 16; j < 64; j++) {
                    int s0 = rotr(w[j - 15], 7) ^ rotr(w[j - 15], 18) ^ (w[j - 15] >>> 3);
                    int s1 = rotr(w[j - 2], 17) ^ rotr(w[j - 2], 19) ^ (w[j - 2] >>> 10);
                    w[j] = w[j - 16] + s0 + w[j - 7] + s1;
                }

                int a = h[0], b = h[1], c = h[2], d = h[3];
                int e = h[4], f = h[5], g = h[6], hh = h[7];

                for (int j = 0; j < 64; j++) {
                    int S1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25);
                    int ch = (e & f) ^ (~e & g);
                    int temp1 = hh + S1 + ch + K[j] + w[j];

                    int S0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22);
                    int maj = (a & b) ^ (a & c) ^ (b & c);
                    int temp2 = S0 + maj;

                    hh = g; g = f; f = e; e = d + temp1;
                    d = c; c = b; b = a; a = temp1 + temp2;
                }

                h[0] += a; h[1] += b; h[2] += c; h[3] += d;
                h[4] += e; h[5] += f; h[6] += g; h[7] += hh;
            }

            StringBuilder hexString = new StringBuilder();
            for (int i : h) {
                String hex = Integer.toHexString(i);
                while (hex.length() < 8) hex = "0" + hex;
                hexString.append(hex);
            }
            return hexString.toString();
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        String testString = "hello world";
        String customHash = SHA256.hash(testString.getBytes());
        String expectedHash = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9";

        if (customHash.equals(expectedHash)) {
            System.out.println("Java SHA-256 Engine Test Passed! Mathematical Bit-Scrambling Verified.");
        } else {
            System.exit(1);
        }
    }
}