class KMPSearch:
    @staticmethod
    def _compute_lps(pattern: str) -> list[int]:
        m = len(pattern)
        lps = [0] * m
        length = 0
        i = 1

        while i < m:
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    @staticmethod
    def search(text: str, pattern: str) -> list[int]:
        n = len(text)
        m = len(pattern)
        if m == 0: return []
        
        lps = KMPSearch._compute_lps(pattern)
        indices = []
        i = 0 # index for text
        j = 0 # index for pattern

        while i < n:
            if pattern[j] == text[i]:
                i += 1
                j += 1

            if j == m:
                indices.append(i - j)
                j = lps[j - 1]
            elif i < n and pattern[j] != text[i]:
                if j != 0:
                    j = lps[j - 1]
                else:
                    i += 1
                    
        return indices

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    dna_sequence = "GACACCCTACACAACCACCACACACCCCCACACAC"
    virus_signature = "ACAC"
    
    matches = KMPSearch.search(dna_sequence, virus_signature)
    
    assert len(matches) == 5, f"Expected 5 matches, found {len(matches)}"
    assert matches == [1, 9, 20, 29, 31], "Incorrect match indices found!"
    
    print("Python KMP Search Test Passed!")