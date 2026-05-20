import hashlib

class MerkleTree:
    def __init__(self, data_blocks):
        self.leaves = [self._hash(block) for block in data_blocks]
        self.tree = []
        self.root = self._build_tree()

    def _hash(self, data: str) -> str:
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def _build_tree(self):
        if not self.leaves:
            return ""
        
        current_level = self.leaves
        self.tree.append(current_level)

        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                # Duplicate the last node if there is an odd number
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                next_level.append(self._hash(left + right))
            
            self.tree.append(next_level)
            current_level = next_level

        return current_level[0]

    def get_root(self):
        return self.root

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    # Simulating 3 transactions
    transactions = ["Tx1: Alice pays Bob 5 BTC", "Tx2: Bob pays Charlie 2 BTC", "Tx3: Charlie pays Dave 1 BTC"]
    
    tree1 = MerkleTree(transactions)
    root1 = tree1.get_root()
    
    # Simulating a hacker altering a single transaction
    hacked_transactions = ["Tx1: Alice pays Bob 5 BTC", "Tx2: Bob pays Hacker 2 BTC", "Tx3: Charlie pays Dave 1 BTC"]
    tree2 = MerkleTree(hacked_transactions)
    root2 = tree2.get_root()
    
    assert root1 != root2, "Merkle Root failed to detect data tampering!"
    assert len(root1) == 64, "SHA-256 hash length is incorrect!"
    
    print("Python Merkle Tree Test Passed!")