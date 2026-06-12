class State:
    def __init__(self, length=0, link=-1):
        self.length = length  
        self.link = link      
        self.transitions = {} 

class SuffixAutomaton:
    def __init__(self, text: str):

        self.states = [State(length=0, link=-1)]
        self.last = 0
        self.size = 1

        for char in text:
            self._extend(char)

    def _extend(self, char: str):
        cur = self.size
        self.states.append(State(length=self.states[self.last].length + 1))
        self.size += 1
        
        p = self.last
        while p != -1 and char not in self.states[p].transitions:
            self.states[p].transitions[char] = cur
            p = self.states[p].link
            
        if p == -1:
            self.states[cur].link = 0
        else:
            q = self.states[p].transitions[char]
            if self.states[p].length + 1 == self.states[q].length:
                self.states[cur].link = q
            else:
                clone = self.size
                self.states.append(State(length=self.states[p].length + 1, link=self.states[q].link))
                self.size += 1

                self.states[clone].transitions = self.states[q].transitions.copy()

                while p != -1 and self.states[p].transitions.get(char) == q:
                    self.states[p].transitions[char] = clone
                    p = self.states[p].link
                    
                self.states[q].link = clone
                self.states[cur].link = clone
                
        self.last = cur

    def contains(self, pattern: str) -> bool:
        """Returns True if the pattern is a substring of the original text."""
        current_state = 0
        for char in pattern:
            if char not in self.states[current_state].transitions:
                return False
            current_state = self.states[current_state].transitions[char]
        return True

if __name__ == '__main__':
    text = "banana"
    sa = SuffixAutomaton(text)
    
    assert sa.size <= 2 * len(text) - 1, "Automaton generated too many states!"

    assert sa.contains("nana") == True
    assert sa.contains("ban") == True
    assert sa.contains("a") == True
    assert sa.contains("nane") == False
    assert sa.contains("apple") == False
    
    print("Python Suffix Automaton Test Passed! O(N) Substring Indexing Verified.")