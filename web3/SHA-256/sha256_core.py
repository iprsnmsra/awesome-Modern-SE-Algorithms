class SHA256:
    # First 32 bits of the fractional parts of the cube roots of the first 64 primes
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    @staticmethod
    def _rotr(x: int, n: int) -> int:
        return ((x >> n) | (x << (32 - n))) & 0xFFFFFFFF

    @staticmethod
    def hash(message: bytes) -> str:
        # Initial Hash Values (Square roots of first 8 primes)
        h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 
             0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]

        # 1. Pre-processing (Padding)
        ml = len(message) * 8
        message += b'\x80'
        while (len(message) * 8) % 512 != 448:
            message += b'\x00'
        message += ml.to_bytes(8, byteorder='big')

        # 2. Process the message in 512-bit (64-byte) chunks
        for i in range(0, len(message), 64):
            chunk = message[i:i+64]
            w = [int.from_bytes(chunk[j:j+4], 'big') for j in range(0, 64, 4)]
            w.extend([0] * 48)

            # Extend the 16 words into 64 words
            for j in range(16, 64):
                s0 = SHA256._rotr(w[j-15], 7) ^ SHA256._rotr(w[j-15], 18) ^ (w[j-15] >> 3)
                s1 = SHA256._rotr(w[j-2], 17) ^ SHA256._rotr(w[j-2], 19) ^ (w[j-2] >> 10)
                w[j] = (w[j-16] + s0 + w[j-7] + s1) & 0xFFFFFFFF

            # Initialize working variables to current hash value
            a, b, c, d, e, f, g, hh = h

            # 3. The 64-Round Compression Loop
            for j in range(64):
                S1 = SHA256._rotr(e, 6) ^ SHA256._rotr(e, 11) ^ SHA256._rotr(e, 25)
                ch = (e & f) ^ ((~e) & g)
                temp1 = (hh + S1 + ch + SHA256.K[j] + w[j]) & 0xFFFFFFFF
                
                S0 = SHA256._rotr(a, 2) ^ SHA256._rotr(a, 13) ^ SHA256._rotr(a, 22)
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = (S0 + maj) & 0xFFFFFFFF

                hh, g, f, e, d, c, b, a = g, f, e, (d + temp1) & 0xFFFFFFFF, c, b, a, (temp1 + temp2) & 0xFFFFFFFF

            # Add the compressed chunk to the current hash value
            for idx, val in enumerate([a, b, c, d, e, f, g, hh]):
                h[idx] = (h[idx] + val) & 0xFFFFFFFF

        # Produce the final hexadecimal string
        return ''.join(f'{val:08x}' for val in h)

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    test_string = "hello world"
    
    # Run our custom implementation
    custom_hash = SHA256.hash(test_string.encode('utf-8'))
    
    # Expected output for "hello world"
    expected_hash = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    
    print(f"Input:    '{test_string}'")
    print(f"Computed: {custom_hash}")
    print(f"Expected: {expected_hash}")
    
    assert custom_hash == expected_hash, "Hash collision! Algorithm failed to strictly compress."
    
    print("\nPython SHA-256 Engine Test Passed! Mathematical Bit-Scrambling Verified.")