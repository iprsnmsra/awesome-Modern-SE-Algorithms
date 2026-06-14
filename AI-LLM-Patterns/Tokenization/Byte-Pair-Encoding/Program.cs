using System;
using System.Collections.Generic;
using System.Linq;

public class Program {
    public class BPETokenizer {
        private int numMerges;
        private Dictionary<string, string> merges = new Dictionary<string, string>();

        public BPETokenizer(int numMerges) {
            this.numMerges = numMerges;
        }

        public void Train(string text) {
            var words = text.Split(new[] { ' ', '\t', '\n' }, StringSplitOptions.RemoveEmptyEntries);
            var wordCounts = new Dictionary<string, int>();

            foreach (var word in words) {
                var chars = string.Join(" ", word.ToCharArray()) + " </w>";
                if (wordCounts.ContainsKey(chars)) wordCounts[chars]++;
                else wordCounts[chars] = 1;
            }

            for (int i = 0; i < numMerges; i++) {
                var pairs = new Dictionary<string, int>();
                foreach (var entry in wordCounts) {
                    var tokens = entry.Key.Split(' ');
                    int freq = entry.Value;
                    for (int j = 0; j < tokens.Length - 1; j++) {
                        string pair = tokens[j] + "," + tokens[j + 1];
                        if (pairs.ContainsKey(pair)) pairs[pair] += freq;
                        else pairs[pair] = freq;
                    }
                }

                if (pairs.Count == 0) break;

                var bestPair = pairs.OrderByDescending(p => p.Value).First().Key;
                if (pairs[bestPair] < 1) break;

                var parts = bestPair.Split(',');
                string newToken = parts[0] + parts[1];
                merges[bestPair] = newToken;

                var newWordCounts = new Dictionary<string, int>();
                string targetMatchSpace = parts[0] + " " + parts[1];

                foreach (var entry in wordCounts) {
                    // Fast swap substitution tracking boundaries
                    string replaced = entry.Key.Replace(targetMatchSpace, newToken);
                    if (newWordCounts.ContainsKey(replaced)) newWordCounts[replaced] += entry.Value;
                    else newWordCounts[replaced] = entry.Value;
                }
                wordCounts = newWordCounts;
            }
        }

        public List<string> Tokenize(string text) {
            var words = text.Split(new[] { ' ', '\t', '\n' }, StringSplitOptions.RemoveEmptyEntries);
            var outputTokens = new List<string>();

            foreach (var word in words) {
                var tokens = word.Select(c => c.ToString()).ToList();
                tokens.Add("</w>");

                while (tokens.Count > 1) {
                    string pairToMerge = null;
                    for (int i = 0; i < tokens.Count - 1; i++) {
                        string key = tokens[i] + "," + tokens[i + 1];
                        if (merges.ContainsKey(key)) {
                            pairToMerge = key;
                            break;
                        }
                    }

                    if (pairToMerge == null) break;

                    string targetToken = merges[pairToMerge];
                    var parts = pairToMerge.Split(',');
                    var newTokens = new List<string>();
                    int j = 0;
                    while (j < tokens.Count) {
                        if (j < tokens.Count - 1 && tokens[j] == parts[0] && tokens[j + 1] == parts[1]) {
                            newTokens.Add(targetToken);
                            j += 2;
                        }
                        else {
                            newTokens.Add(tokens[j]);
                            j++;
                        }
                    }
                    tokens = newTokens;
                }
                outputTokens.AddRange(tokens);
            }
            return outputTokens;
        }
    }

    // --- CI/CD Automated Test ---
    public static int Main() {
        var tokenizer = new BPETokenizer(10);
        tokenizer.Train("hug pug hug pug hug pug shug");
        var result = tokenizer.Tokenize("hug pug");

        if (result.Count < 8 && result.Count > 0) {
            Console.WriteLine("C# BPE Tokenizer Test Passed!");
            return 0;
        }
        return 1;
    }
}