#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <iomanip>
#include <functional>
#include <cassert>

// Note: Using std::hash for zero-dependency CI/CD compilation. 
// In a true production environment, you would use OpenSSL for SHA-256.
class MerkleTree {
private:
    std::string root;

    std::string hash(const std::string& data) {
        std::hash<std::string> hasher;
        size_t h = hasher(data);
        std::stringstream ss;
        ss << std::hex << std::setw(16) << std::setfill('0') << h;
        return ss.str();
    }

    std::string buildTree(std::vector<std::string> currentLevel) {
        if (currentLevel.empty()) return "";
        if (currentLevel.size() == 1) return currentLevel[0];

        std::vector<std::string> nextLevel;
        for (size_t i = 0; i < currentLevel.size(); i += 2) {
            std::string left = currentLevel[i];
            std::string right = (i + 1 < currentLevel.size()) ? currentLevel[i + 1] : left;
            nextLevel.push_back(hash(left + right));
        }
        return buildTree(nextLevel);
    }

public:
    MerkleTree(const std::vector<std::string>& dataBlocks) {
        std::vector<std::string> leaves;
        for (const auto& block : dataBlocks) {
            leaves.push_back(hash(block));
        }
        root = buildTree(leaves);
    }

    std::string getRoot() const {
        return root;
    }
};

// --- CI/CD Automated Test ---
int main() {
    std::vector<std::string> data = {"Doc1", "Doc2", "Doc3"};
    MerkleTree tree1(data);

    std::vector<std::string> hackedData = {"Doc1", "HACKED_DOC", "Doc3"};
    MerkleTree tree2(hackedData);

    assert(tree1.getRoot() != tree2.getRoot());
    std::cout << "C++ Merkle Tree Test Passed!\n";
    return 0;
}