import java.util.*;

public class Main {
    static class BPETokenizer {
        private final int numMerges;
        private final Map<String, String> merges = new LinkedHashMap<>();

        public BPETokenizer(int numMerges) {
            this.numMerges = numMerges;
        }

        public void train(String text) {
            String[] words = text.split("\\s+");
            Map<List<String>, Integer> wordCounts = new HashMap<>();

            for (String word : words) {
                if (word.isEmpty()) continue;
                List<String> split = new ArrayList<>(Arrays.asList(word.split("")));
                split.add("</w>");
                wordCounts.put(split, wordCounts.getOrDefault(split, 0) + 1);
            }

            for (int i = 0; i < numMerges; i++) {
                Map<String, Integer> pairs = new HashMap<>();

                for (Map.Entry<List<String>, Integer> entry : wordCounts.entrySet()) {
                    List<String> wordTuple = entry.getKey();
                    int freq = entry.getValue();
                    for (int j = 0; j < wordTuple.size() - 1; j++) {
                        String pairStr = wordTuple.get(j) + "," + wordTuple.get(j + 1);
                        pairs.put(pairStr, pairs.getOrDefault(pairStr, 0) + freq);
                    }
                }

                if (pairs.isEmpty()) break;

                String bestPairStr = null;
                int maxFreq = -1;
                for (Map.Entry<String, Integer> pairEntry : pairs.entrySet()) {
                    if (pairEntry.getValue() > maxFreq) {
                        maxFreq = pairEntry.getValue();
                        bestPairStr = pairEntry.getKey();
                    }
                }

                if (maxFreq < 1) break;

                String[] parts = bestPairStr.split(",");
                String newToken = parts[0] + parts[1];
                merges.put(bestPairStr, newToken);

                Map<List<String>, Integer> newWordCounts = new HashMap<>();
                for (Map.Entry<List<String>, Integer> entry : wordCounts.entrySet()) {
                    List<String> wordTuple = entry.getKey();
                    int freq = entry.getValue();
                    List<String> newWord = new ArrayList<>();
                    int j = 0;
                    while (j < wordTuple.size()) {
                        if (j < wordTuple.size() - 1 && wordTuple.get(j).equals(parts[0]) && wordTuple.get(j + 1).equals(parts[1])) {
                            newWord.add(newToken);
                            j += 2;
                        } else {
                            newWord.add(wordTuple.get(j));
                            j++;
                        }
                    }
                    newWordCounts.put(newWord, freq);
                }
                wordCounts = newWordCounts;
            }
        }

        public List<String> tokenize(String text) {
            String[] words = text.split("\\s+");
            List<String> outputTokens = new ArrayList<>();

            for (String word : words) {
                if (word.isEmpty()) continue;
                List<String> tokens = new ArrayList<>(Arrays.asList(word.split("")));
                tokens.add("</w>");

                while (tokens.size() > 1) {
                    String pairToMerge = null;

                    for (int i = 0; i < tokens.size() - 1; i++) {
                        String checkKey = tokens.get(i) + "," + tokens.get(i + 1);
                        if (merges.containsKey(checkKey)) {
                            pairToMerge = checkKey;
                            break;
                        }
                    }

                    if (pairToMerge == null) break;

                    String targetToken = merges.get(pairToMerge);
                    String[] parts = pairToMerge.split(",");
                    List<String> newTokens = new ArrayList<>();
                    int i = 0;
                    while (i < tokens.size()) {
                        if (i < tokens.size() - 1 && tokens.get(i).equals(parts[0]) && tokens.get(i + 1).equals(parts[1])) {
                            newTokens.add(targetToken);
                            i += 2;
                        } else {
                            newTokens.add(tokens.get(i));
                            i++;
                        }
                    }
                    tokens = newTokens;
                }
                outputTokens.addAll(tokens);
            }
            return outputTokens;
        }
    }

    // --- CI/CD Automated Test ---
    public static void main(String[] args) {
        BPETokenizer tokenizer = new BPETokenizer(10);
        tokenizer.train("hug pug hug pug hug pug shug");
        List<String> result = tokenizer.tokenize("hug pug");

        if (result.size() < 8 && !result.isEmpty()) {
            System.out.println("Java BPE Tokenizer Test Passed!");
        } else {
            System.exit(1);
        }
    }
}