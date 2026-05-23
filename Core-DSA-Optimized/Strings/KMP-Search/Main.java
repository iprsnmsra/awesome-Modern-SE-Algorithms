import java.util.ArrayList;
import java.util.List;

public class Main {
    static class KMPSearch {
        private static int[] computeLPS(String pattern) {
            int m = pattern.length();
            int[] lps = new int[m];
            int len = 0;
            int i = 1;
            
            while (i < m) {
                if (pattern.charAt(i) == pattern.charAt(len)) {
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

        public static List<Integer> search(String text, String pattern) {
            List<Integer> indices = new ArrayList<>();
            int n = text.length();
            int m = pattern.length();
            if (m == 0) return indices;

            int[] lps = computeLPS(pattern);
            int i = 0;
            int j = 0;

            while (i < n) {
                if (pattern.charAt(j) == text.charAt(i)) {
                    i++;
                    j++;
                }
                if (j == m) {
                    indices.add(i - j);
                    j = lps[j - 1];
                } else if (i < n && pattern.charAt(j) != text.charAt(i)) {
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
    public static void main(String[] args) {
        String text = "GACACCCTACACAACCACCACACACCCCCACACAC";
        String pattern = "ACAC";
        
        List<Integer> matches = KMPSearch.search(text, pattern);
        
        if (matches.size() == 5 && matches.get(0) == 1 && matches.get(4) == 31) {
            System.out.println("Java KMP Search Test Passed!");
        } else {
            System.exit(1);
        }
    }
}