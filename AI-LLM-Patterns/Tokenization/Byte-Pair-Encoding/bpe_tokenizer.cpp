#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <sstream>
#include <algorithm>
#include <cassert>

using namespace std;

class BPETokenizer {
private:
    int numMerges;
    map<pair<string, string>, string> merges;

public:
    BPETokenizer(int mergesCount) : numMerges(mergesCount) {}

    void train(const string& text) {
        stringstream ss(text);
        string word;
        map<vector<string>, int> wordCounts;

        while (ss >> word) {
            vector<string> split;
            for (char c : word) {
                split.push_back(string(1, c));
            }
            split.push_back("</w>");
            wordCounts[split]++;
        }

        for (int i = 0; i < numMerges; i++) {
            map<pair<string, string>, int> pairs;

            for (auto const& [wordTuple, freq] : wordCounts) {
                if (wordTuple.size() < 2) continue;
                for (size_t j = 0; j < wordTuple.size() - 1; j++) {
                    pairs[{wordTuple[j], wordTuple[j + 1]}] += freq;
                }
            }

            if (pairs.empty()) break;

            pair<string, string> bestPair;
            int maxFreq = -1;
            for (auto const& [pair, freq] : pairs) {
                if (freq > maxFreq) {
                    maxFreq = freq;
                    bestPair = pair;
                }
            }

            if (maxFreq < 1) break;

            string newToken = bestPair.first + bestPair.second;
            merges[bestPair] = newToken;

            map<vector<string>, int> newWordCounts;
            for (auto const& [wordTuple, freq] : wordCounts) {
                vector<string> newWord;
                size_t j = 0;
                while (j < wordTuple.size()) {
                    if (j < wordTuple.size() - 1 && wordTuple[j] == bestPair.first && wordTuple[j + 1] == bestPair.second) {
                        newWord.push_back(newToken);
                        j += 2;
                    } else {
                        newWord.push_back(wordTuple[j]);
                        j++;
                    }
                }
                newWordCounts[newWord] = freq;
            }
            wordCounts = newWordCounts;
        }
    }

    vector<string> tokenize(const string& text) {
        stringstream ss(text);
        string word;
        vector<string> outputTokens;

        while (ss >> word) {
            vector<string> tokens;
            for (char c : word) {
                tokens.push_back(string(1, c));
            }
            tokens.push_back("</w>");

            while (tokens.size() > 1) {
                bool mergedAny = false;
                
                for (size_t i = 0; i < tokens.size() - 1; i++) {
                    auto checkPair = make_pair(tokens[i], tokens[i + 1]);
                    if (merges.find(checkPair) != merges.end()) {
                        string targetToken = merges[checkPair];
                        vector<string> newTokens;
                        size_t j = 0;
                        while (j < tokens.size()) {
                            if (j < tokens.size() - 1 && tokens[j] == checkPair.first && tokens[j + 1] == checkPair.second) {
                                newTokens.push_back(targetToken);
                                j += 2;
                            } else {
                                newTokens.push_back(tokens[j]);
                                j++;
                            }
                        }
                        tokens = newTokens;
                        mergedAny = true;
                        break;
                    }
                }
                if (!mergedAny) break;
            }
            for (const auto& token : tokens) {
                outputTokens.push_back(token);
            }
        }
        return outputTokens;
    }
};

int main() {
    BPETokenizer tokenizer(10);
    tokenizer.train("hug pug hug pug hug pug shug");
    vector<string> result = tokenizer.tokenize("hug pug");

    assert(result.size() < 8);
    assert(!result.empty());

    cout << "C++ BPE Tokenizer Test Passed!\n";
    return 0;
}