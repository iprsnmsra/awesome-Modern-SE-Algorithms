using System;
using System.Collections.Generic;

public class Program {
    class KMPSearch {
        private static int[] ComputeLPS(string pattern) {
            int m = pattern.Length;
            int[] lps = new int[m];
            int len = 0;
            int i = 1;

            while (i < m) {
                if (pattern[i] == pattern[len]) {
                    len++;
                    lps[i] = len;
                    i++;
                } else {
                    if (len != 0) {
                        len = lps[len - 1];
                    } else {
                        lps[i] = 0;
                        i++;
                    }
                }
            }
            return lps;
        }

        public static List<int> Search(string text, string pattern) {
            var indices = new List<int>();
            int n = text.Length;
            int m = pattern.Length;
            if (m == 0) return indices;

            int[] lps = ComputeLPS(pattern);
            int i = 0; 
            int j = 0;

            while (i < n) {
                if (pattern[j] == text[i]) {
                    i++;
                    j++;
                }
                if (j == m) {
                    indices.Add(i - j);
                    j = lps[j - 1];
                } else if (i < n && pattern[j] != text[i]) {
                    if (j != 0) {
                        j = lps[j - 1];
                    } else {
                        i++;
                    }
                }
            }
            return indices;
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        string text = "GACACCCTACACAACCACCACACACCCCCACACAC";
        string pattern = "ACAC";
        
        var matches = KMPSearch.Search(text, pattern);
        
        if (matches.Count == 5 && matches[0] == 1 && matches[4] == 31) {
            Console.WriteLine("C# KMP Search Test Passed!");
            return 0;
        }
        return 1;
    }
}