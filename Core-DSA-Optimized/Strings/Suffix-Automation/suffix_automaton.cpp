#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
#include <cassert>

using namespace std;

struct State {
    int length;
    int link;
    unordered_map<char, int> transitions;
    
    State(int l, int lnk) : length(l), link(lnk) {}
};

class SuffixAutomaton {
private:
    vector<State> states;
    int last;

    void extend(char c) {
        int cur = size++;
        states.emplace_back(states[last].length + 1, 0);
        
        int p = last;
        while (p != -1 && states[p].transitions.find(c) == states[p].transitions.end()) {
            states[p].transitions[c] = cur;
            p = states[p].link;
        }

        if (p == -1) {
            states[cur].link = 0;
        } else {
            int q = states[p].transitions[c];
            if (states[p].length + 1 == states[q].length) {
                states[cur].link = q;
            } else {
                int clone = size++;
                states.emplace_back(states[p].length + 1, states[q].link);
                states[clone].transitions = states[q].transitions;
                
                while (p != -1 && states[p].transitions[c] == q) {
                    states[p].transitions[c] = clone;
                    p = states[p].link;
                }
                
                states[q].link = clone;
                states[cur].link = clone;
            }
        }
        last = cur;
    }

public:
    int size;

    SuffixAutomaton(const string& text) {
        states.reserve(2 * text.length());
        states.emplace_back(0, -1);
        last = 0;
        size = 1;
        
        for (char c : text) {
            extend(c);
        }
    }

    bool contains(const string& pattern) {
        int currentState = 0;
        for (char c : pattern) {
            if (states[currentState].transitions.find(c) == states[currentState].transitions.end()) {
                return false;
            }
            currentState = states[currentState].transitions[c];
        }
        return true;
    }
};
int main() {
    string text = "banana";
    SuffixAutomaton sa(text);

    assert(sa.size <= 2 * text.length() - 1);
    assert(sa.contains("nana") == true);
    assert(sa.contains("ban") == true);
    assert(sa.contains("apple") == false);

    cout << "C++ Suffix Automaton Test Passed! O(N) Substring Indexing Verified.\n";
    return 0;
}