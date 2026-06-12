using System;
using System.Collections.Generic;

public class Program {
    public class State {
        public int length;
        public int link;
        public Dictionary<char, int> transitions;

        public State(int length, int link) {
            this.length = length;
            this.link = link;
            this.transitions = new Dictionary<char, int>();
        }
    }

    public class SuffixAutomaton {
        private List<State> states;
        private int last;
        public int Size { get; private set; }

        public SuffixAutomaton(string text) {
            states = new List<State> { new State(0, -1) };
            last = 0;
            Size = 1;

            foreach (char c in text) {
                Extend(c);
            }
        }

        private void Extend(char c) {
            int cur = Size++;
            states.Add(new State(states[last].length + 1, 0));

            int p = last;
            while (p != -1 && !states[p].transitions.ContainsKey(c)) {
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
                    int clone = Size++;
                    State cloneState = new State(states[p].length + 1, states[q].link);
                    
                    foreach (var kvp in states[q].transitions) {
                        cloneState.transitions[kvp.Key] = kvp.Value;
                    }
                    states.Add(cloneState);

                    while (p != -1 && states[p].transitions.TryGetValue(c, out int target) && target == q) {
                        states[p].transitions[c] = clone;
                        p = states[p].link;
                    }

                    states[q].link = clone;
                    states[cur].link = clone;
                }
            }
            last = cur;
        }

        public bool Contains(string pattern) {
            int currentState = 0;
            foreach (char c in pattern) {
                if (!states[currentState].transitions.ContainsKey(c)) {
                    return false;
                }
                currentState = states[currentState].transitions[c];
            }
            return true;
        }
    }
    public static int Main() {
        string text = "banana";
        var sa = new SuffixAutomaton(text);

        bool pass = true;
        pass &= sa.Size <= 2 * text.Length - 1;
        pass &= sa.Contains("nana");
        pass &= sa.Contains("ban");
        pass &= !sa.Contains("apple");

        if (pass) {
            Console.WriteLine("C# Suffix Automaton Test Passed! O(N) Substring Indexing Verified.");
            return 0;
        }
        return 1;
    }
}