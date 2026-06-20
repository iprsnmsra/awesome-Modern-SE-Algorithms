import random

class PedersenCommitment:
    def __init__(self):
        # In production, P and Q would be massive 256-bit prime numbers.
        # For CI/CD execution speed, we use smaller, safe prime fields.
        self.p = 2083  # The finite field prime
        self.g = 2     # First publicly known generator
        self.h = 3     # Second publicly known generator (relationship to g is unknown)

    def generate_blinding_factor(self) -> int:
        """Generates a random secret r used to completely cloak the value."""
        return random.randint(1, self.p - 1)

    def commit(self, value: int, blinding_factor: int) -> int:
        """
        Creates the commitment: C = (g^v * h^r) mod p
        """
        c_v = pow(self.g, value, self.p)
        c_r = pow(self.h, blinding_factor, self.p)
        return (c_v * c_r) % self.p

    def verify(self, commitment: int, value: int, blinding_factor: int) -> bool:
        """Proves that a specific value and blinding factor map to the given commitment."""
        expected_commitment = self.commit(value, blinding_factor)
        return expected_commitment == commitment

    def homomorphic_add(self, c1: int, c2: int) -> int:
        """
        Multiplication in this prime field equates to adding the underlying values.
        C1 * C2 = (g^v1 * h^r1) * (g^v2 * h^r2) = g^(v1+v2) * h^(r1+r2)
        """
        return (c1 * c2) % self.p

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    crypto = PedersenCommitment()
    
    # 1. Alice commits to sending exactly 5 coins
    alice_value = 5
    alice_blinding = crypto.generate_blinding_factor()
    alice_commitment = crypto.commit(alice_value, alice_blinding)
    
    print(f"Alice's Secret Value: {alice_value}")
    print(f"Alice's Public Commitment: {alice_commitment}")
    
    # 2. Bob commits to sending exactly 10 coins
    bob_value = 10
    bob_blinding = crypto.generate_blinding_factor()
    bob_commitment = crypto.commit(bob_value, bob_blinding)
    
    # 3. The Blockchain Network homomorphically adds the commitments together
    # The network DOES NOT know Alice sent 5 or Bob sent 10.
    network_sum_commitment = crypto.homomorphic_add(alice_commitment, bob_commitment)
    
    # 4. Verification
    # To prove the network sum is correct, we provide the sum of the values and blinding factors.
    combined_value = alice_value + bob_value
    combined_blinding = alice_blinding + bob_blinding
    
    is_valid = crypto.verify(network_sum_commitment, combined_value, combined_blinding)
    assert is_valid == True, "Homomorphic addition failed verification!"
    
    # 5. Hacker attempts to fake the value
    is_fake_valid = crypto.verify(network_sum_commitment, 999, combined_blinding)
    assert is_fake_valid == False, "Security Breach! Commitment is not perfectly binding."
    
    print("\nPython Pedersen Commitment Test Passed! Homomorphic Confidential Transactions Verified.")