import random

class SchnorrZKP:
    def __init__(self, p: int, g: int):
        # Public parameters
        self.p = p # A prime number
        self.g = g # A generator

    def mod_exp(self, base: int, exp: int) -> int:
        # Fast modular exponentiation: (base^exp) % p
        return pow(base, exp, self.p)

    def generate_keys(self, secret_x: int) -> int:
        # Public Key (y) = g^x mod p
        return self.mod_exp(self.g, secret_x)

    def prove_and_verify(self, secret_x: int, public_y: int) -> bool:
        print(f"[Prover] Secret (x) is {secret_x}. (This never leaves the Prover's machine)")
        
        # --- STEP 1: PROVER COMMITMENT ---
        # Prover generates a random k, computes r = g^k mod p, and sends r to Verifier.
        k = random.randint(1, self.p - 2)
        r = self.mod_exp(self.g, k)
        print(f"[Prover] Sends Commitment (r): {r}")

        # --- STEP 2: VERIFIER CHALLENGE ---
        # Verifier generates a random challenge c and sends to Prover.
        c = random.randint(1, self.p - 2)
        print(f"[Verifier] Sends Challenge (c): {c}")

        # --- STEP 3: PROVER RESPONSE ---
        # Prover computes s = k + c * x and sends to Verifier.
        s = k + c * secret_x
        print(f"[Prover] Sends Response (s): {s}")

        # --- STEP 4: VERIFICATION ---
        # Verifier checks if g^s mod p == (r * y^c) mod p
        # If true, Prover mathematically proved they know 'x' without revealing it.
        
        # Left side: g^s mod p
        left_side = self.mod_exp(self.g, s)
        
        # Right side: (r * y^c) mod p
        y_c = self.mod_exp(public_y, c)
        right_side = (r * y_c) % self.p
        
        print(f"[Verifier] Checks if {left_side} == {right_side}")
        return left_side == right_side

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    # Using a small prime group for CI/CD speed
    prime_p = 23
    generator_g = 5
    
    zkp = SchnorrZKP(prime_p, generator_g)
    
    # Alice's super secret password/key
    alice_secret = 7
    alice_public = zkp.generate_keys(alice_secret)
    
    print(f"--- Schnorr ZKP Protocol Started ---")
    is_verified = zkp.prove_and_verify(alice_secret, alice_public)
    
    assert is_verified == True, "Zero-Knowledge Proof failed mathematically!"
    print("\nPython Zero-Knowledge Proof Test Passed!")