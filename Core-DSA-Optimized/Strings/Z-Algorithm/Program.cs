using System;
using System.Collections.Generic;

public class Program {
    public class ZAlgorithm {
        private static int[] GetZArray(string s) {
            int n = s.Length;
            int[] z = new int[n];
            int L = 0, R = 0;

            for (int i = 1; i < n; i++) {
                if (i <= R) {
                    z[i] = Math.Min(R - i + 1, z[i - L]);
                }

                while (i + z[i] < n && s[z[i]] == s[i + z[i]]) {
                    z[i]++;
                }

                if (i + z[i] - 1 > R) {
                    L = i;
                    R = i + z[i] - 1;
                }
            }

            return z;
        }

        public static List<int> Search(string pattern, string text) {
            var matches = new List<int>();
            if (string.IsNullOrEmpty(pattern) || string.IsNullOrEmpty(text)) {
                return matches;
            }

            string concat = pattern + "$" + text;
            int m = pattern.Length;
            int[] zArray = GetZArray(concat);

            for (int i = 0; i < zArray.Length; i++) {
                if (zArray[i] == m) {
                    matches.Add(i - m - 1);
                }
            }

            return matches;
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        string text = "AABAACAADAABAABA";
        string pattern = "AABA";

        List<int> results = ZAlgorithm.Search(pattern, text);

        if (results.Count == 3 && results[0] == 0 && results[1] == 9 && results[2] == 12) {
            Console.WriteLine("C# Z-Algorithm Pattern Matching Test Passed!");
            return 0;
        }
        
        return 1;
    }
}