import java.util.ArrayList;
import java.util.List;

public class Main {
    static class ZAlgorithm {
        private static int[] getZArray(String s) {
            int n = s.length();
            int[] z = new int[n];
            int L = 0, R = 0;

            for (int i = 1; i < n; i++) {
                if (i <= R) {
                    z[i] = Math.min(R - i + 1, z[i - L]);
                }

                while (i + z[i] < n && s.charAt(z[i]) == s.charAt(i + z[i])) {
                    z[i]++;
                }

                if (i + z[i] - 1 > R) {
                    L = i;
                    R = i + z[i] - 1;
                }
            }

            return z;
        }

        public static List<Integer> search(String pattern, String text) {
            List<Integer> matches = new ArrayList<>();
            if (pattern == null || pattern.isEmpty() || text == null || text.isEmpty()) {
                return matches;
            }

            String concat = pattern + "$" + text;
            int m = pattern.length();
            int[] zArray = getZArray(concat);

            for (int i = 0; i < zArray.length; i++) {
                if (zArray[i] == m) {
                    matches.add(i - m - 1);
                }
            }

            return matches;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        String text = "AABAACAADAABAABA";
        String pattern = "AABA";

        List<Integer> results = ZAlgorithm.search(pattern, text);

        if (results.size() == 3 && results.get(0) == 0 && results.get(1) == 9 && results.get(2) == 12) {
            System.out.println("Java Z-Algorithm Pattern Matching Test Passed!");
        } else {
            System.exit(1);
        }
    }
}