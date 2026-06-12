import java.util.HashMap;
import java.util.ArrayList;
import java.util.Map;

public class Main {
    static class State {
        int length;
        int link;
        Map<Character, Integer> transitions;

        public State(int length, int link) {
            this.length = length;
            this.link = link;
            this.transitions = new HashMap<>();
        }
    }

    static class SuffixAutomaton {
        ArrayList<State> states;
        int last;
        int size;

        public SuffixAutomaton(String text) {
            states = new ArrayList<>();
            states.add(new State(0, -1));
            last = 0;
            size = 1;

            for (char c : text.toCharArray()) {
                extend(c);
            }
        }

        private void extend(char c) {
            int cur = size++;
            states.add(new State(states.get(last).length + 1, 0));

            int p = last;
            while (p != -1 && !states.get(p).transitions.containsKey(c)) {
                states.get(p).transitions.put(c, cur);
                p = states.get(p).link;
            }

            if (p == -1) {
                states.get(cur).link = 0;
            } else {
                int q = states.get(p).transitions.get(c);
                if (states.get(p).length + 1 == states.get(q).length) {
                    states.get(cur).link = q;
                } else {
                    int clone = size++;
                    State cloneState = new State(states.get(p).length + 1, states.get(q).link);
                    cloneState.transitions.putAll(states.get(q).transitions);
                    states.add(cloneState);

                    while (p != -1 && states.get(p).transitions.getOrDefault(c, -1) == q) {
                        states.get(p).transitions.put(c, clone);
                        p = states.get(p).link;
                    }

                    states.get(q).link = clone;
                    states.get(cur).link = clone;
                }
            }
            last = cur;
        }

        public boolean contains(String pattern) {
            int currentState = 0;
            for (char c : pattern.toCharArray()) {
                if (!states.get(currentState).transitions.containsKey(c)) {
                    return false;
                }
                currentState = states.get(currentState).transitions.get(c);
            }
            return true;
        }
    }

    public static void main(String[] args) {
        String text = "banana";
        SuffixAutomaton sa = new SuffixAutomaton(text);

        boolean pass = true;
        pass &= sa.size <= 2 * text.length() - 1;
        pass &= sa.contains("nana");
        pass &= sa.contains("ban");
        pass &= !sa.contains("apple");

        if (pass) {
            System.out.println("Java Suffix Automaton Test Passed! O(N) Substring Indexing Verified.");
        } else {
            System.exit(1);
        }
    }
}