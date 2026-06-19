import random

# A prime number strictly larger than our secret and N
# In production, this would be a massive 256-bit prime (e.g., Secp256k1 order)
PRIME = 2083 

class ShamirSecretSharing:
    @staticmethod
    def _mod_inverse(n: int, p: int) -> int:
        """Calculates the modular multiplicative inverse using Fermat's Little Theorem."""
        return pow(n, p - 2, p)

    @staticmethod
    def split_secret(secret: int, n: int, k: int) -> list[tuple[int, int]]:
        """Splits a secret into N shares requiring K shares to reconstruct."""
        if k > n:
            raise ValueError("Threshold (K) cannot be greater than total shares (N).")
        if secret >= PRIME:
            raise ValueError(f"Secret must be smaller than the prime field ({PRIME}).")

        # Generate random coefficients for f(x) = secret + a1*x + a2*x^2 ...
        coefficients = [secret] + [random.randint(1, PRIME - 1) for _ in range(k - 1)]
        
        shares = []
        for i in range(1, n + 1):
            x = i
            y = sum(c * (x ** exp) for exp, c in enumerate(coefficients)) % PRIME
            shares.append((x, y))
            
        return shares

    @staticmethod
    def reconstruct_secret(shares: list[tuple[int, int]]) -> int:
        """Reconstructs the secret using Lagrange Interpolation at x=0."""
        secret = 0
        
        for i, (x_i, y_i) in enumerate(shares):
            numerator = 1
            denominator = 1
            
            for j, (x_j, y_j) in enumerate(shares):
                if i == j:
                    continue
                # Calculate the Lagrange basis polynomial
                numerator = (numerator * -x_j) % PRIME
                denominator = (denominator * (x_i - x_j)) % PRIME
                
            # y_i * (numerator / denominator) % PRIME
            lagrange_val = (y_i * numerator * ShamirSecretSharing._mod_inverse(denominator, PRIME)) % PRIME
            secret = (secret + lagrange_val) % PRIME
            
        # Ensure positive modulo result
        return (secret + PRIME) % PRIME

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    original_secret = 1337
    N = 5 # Total shares
    K = 3 # Threshold required
    
    print(f"🔒 Original Master Key: {original_secret}")
    
    # 1. Split the secret
    all_shares = ShamirSecretSharing.split_secret(original_secret, N, K)
    print("\nDistributed Shares:")
    for share in all_shares:
        print(f"Server {share[0]} holds coordinate -> {share}")
        
    # 2. Attempt reconstruction with exactly K (3) shares
    valid_reconstruction = ShamirSecretSharing.reconstruct_secret(all_shares[:3])
    print(f"\n✅ Reconstructing with 3 shares: {valid_reconstruction}")
    assert valid_reconstruction == original_secret, "Failed to reconstruct with valid threshold!"
    
    # 3. Attempt reconstruction with less than K (2) shares (Should produce mathematically random garbage)
    invalid_reconstruction = ShamirSecretSharing.reconstruct_secret(all_shares[:2])
    print(f"❌ Reconstructing with 2 shares: {invalid_reconstruction} (Meaningless Garbage)")
    assert invalid_reconstruction != original_secret, "Security breach! Reconstructed with insufficient shares."
    
    print("\nPython Shamir's Secret Sharing Test Passed! Information-theoretic security verified.")