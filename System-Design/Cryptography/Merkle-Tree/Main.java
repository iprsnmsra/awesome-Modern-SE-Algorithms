import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.List;

public class Main {
    static class MerkleTree {
        private List<String> leaves;
        private String root;

        public MerkleTree(List<String> dataBlocks) {
            leaves = new ArrayList<>();
            for (String block : dataBlocks) {
                leaves.add(hash(block));
            }
            root = buildTree(leaves);
        }

        private String hash(String data) {
            try {
                MessageDigest digest = MessageDigest.getInstance("SHA-256");
                byte[] hashBytes = digest.digest(data.getBytes("UTF-8"));
                StringBuilder hexString = new StringBuilder();
                for (byte b : hashBytes) {
                    String hex = Integer.toHexString(0xff & b);
                    if (hex.length() == 1) hexString.append('0');
                    hexString.append(hex);
                }
                return hexString.toString();
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        }

        private String buildTree(List<String> currentLevel) {
            if (currentLevel.isEmpty()) return "";
            if (currentLevel.size() == 1) return currentLevel.get(0);

            List<String> nextLevel = new ArrayList<>();
            for (int i = 0; i < currentLevel.size(); i += 2) {
                String left = currentLevel.get(i);
                String right = (i + 1 < currentLevel.size()) ? currentLevel.get(i + 1) : left;
                nextLevel.add(hash(left + right));
            }
            return buildTree(nextLevel);
        }

        public String getRoot() {
            return root;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        List<String> data = List.of("Data A", "Data B", "Data C");
        MerkleTree tree1 = new MerkleTree(data);

        List<String> hackedData = List.of("Data A", "HACKED B", "Data C");
        MerkleTree tree2 = new MerkleTree(hackedData);

        if (!tree1.getRoot().equals(tree2.getRoot())) {
            System.out.println("Java Merkle Tree Test Passed!");
        } else {
            System.exit(1);
        }
    }
}