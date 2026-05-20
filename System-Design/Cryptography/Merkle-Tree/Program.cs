using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;

public class Program {
    class MerkleTree {
        private List<string> leaves;
        private string root;

        public MerkleTree(List<string> dataBlocks) {
            leaves = dataBlocks.Select(Hash).ToList();
            root = BuildTree(leaves);
        }

        private string Hash(string data) {
            using (SHA256 sha256Hash = SHA256.Create()) {
                byte[] bytes = sha256Hash.ComputeHash(Encoding.UTF8.GetBytes(data));
                StringBuilder builder = new StringBuilder();
                foreach (byte b in bytes) {
                    builder.Append(b.ToString("x2"));
                }
                return builder.ToString();
            }
        }

        private string BuildTree(List<string> currentLevel) {
            if (currentLevel.Count == 0) return "";
            if (currentLevel.Count == 1) return currentLevel[0];

            List<string> nextLevel = new List<string>();
            for (int i = 0; i < currentLevel.Count; i += 2) {
                string left = currentLevel[i];
                string right = (i + 1 < currentLevel.Count) ? currentLevel[i + 1] : left;
                nextLevel.Add(Hash(left + right));
            }
            return BuildTree(nextLevel);
        }

        public string GetRoot() {
            return root;
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var txs = new List<string> { "Node 1", "Node 2", "Node 3" };
        var tree1 = new MerkleTree(txs);

        var hackedTxs = new List<string> { "Node 1", "CORRUPT", "Node 3" };
        var tree2 = new MerkleTree(hackedTxs);

        if (tree1.GetRoot() != tree2.GetRoot()) {
            Console.WriteLine("C# Merkle Tree Test Passed!");
            return 0;
        }
        return 1;
    }
}