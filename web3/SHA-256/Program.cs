using System;
using System.Text;
using System.Collections.Generic;

public class Program {
    public class SHA256 {
        private static readonly uint[] K = {
            0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
            0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
            0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
            0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
            0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
            0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
            0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
            0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
        };

        private static uint Rotr(uint x, int n) {
            return (x >> n) | (x << (32 - n));
        }

        public static string Hash(string message) {
            uint[] h = {
                0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
                0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
            };

            byte[] msgBytes = Encoding.UTF8.GetBytes(message);
            ulong bitLen = (ulong)msgBytes.Length * 8;

            var paddedMsg = new List<byte>(msgBytes);
            paddedMsg.Add(0x80);
            while ((paddedMsg.Count * 8) % 512 != 448) {
                paddedMsg.Add(0x00);
            }

            for (int i = 7; i >= 0; i--) {
                paddedMsg.Add((byte)(bitLen >> (i * 8)));
            }

            for (int i = 0; i < paddedMsg.Count; i += 64) {
                uint[] w = new uint[64];
                for (int j = 0; j < 16; j++) {
                    w[j] = ((uint)paddedMsg[i + j * 4] << 24) |
                           ((uint)paddedMsg[i + j * 4 + 1] << 16) |
                           ((uint)paddedMsg[i + j * 4 + 2] << 8) |
                           ((uint)paddedMsg[i + j * 4 + 3]);
                }

                for (int j = 16; j < 64; j++) {
                    uint s0 = Rotr(w[j - 15], 7) ^ Rotr(w[j - 15], 18) ^ (w[j - 15] >> 3);
                    uint s1 = Rotr(w[j - 2], 17) ^ Rotr(w[j - 2], 19) ^ (w[j - 2] >> 10);
                    w[j] = w[j - 16] + s0 + w[j - 7] + s1;
                }

                uint a = h[0], b = h[1], c = h[2], d = h[3];
                uint e = h[4], f = h[5], g = h[6], hh = h[7];

                for (int j = 0; j < 64; j++) {
                    uint S1 = Rotr(e, 6) ^ Rotr(e, 11) ^ Rotr(e, 25);
                    uint ch = (e & f) ^ (~e & g);
                    uint temp1 = hh + S1 + ch + K[j] + w[j];

                    uint S0 = Rotr(a, 2) ^ Rotr(a, 13) ^ Rotr(a, 22);
                    uint maj = (a & b) ^ (a & c) ^ (b & c);
                    uint temp2 = S0 + maj;

                    hh = g; g = f; f = e; e = d + temp1;
                    d = c; c = b; b = a; a = temp1 + temp2;
                }

                h[0] += a; h[1] += b; h[2] += c; h[3] += d;
                h[4] += e; h[5] += f; h[6] += g; h[7] += hh;
            }

            var result = new StringBuilder();
            foreach (uint val in h) {
                result.Append(val.ToString("x8"));
            }
            return result.ToString();
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        string testString = "hello world";
        string customHash = SHA256.Hash(testString);
        string expectedHash = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9";

        if (customHash == expectedHash) {
            Console.WriteLine("C# SHA-256 Engine Test Passed! Mathematical Bit-Scrambling Verified.");
            return 0;
        }
        return 1;
    }
}