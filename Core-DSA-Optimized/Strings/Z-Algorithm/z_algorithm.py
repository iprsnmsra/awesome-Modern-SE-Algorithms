class ZAlgorithm:
    @staticmethod
    def _get_z_array(s: str) -> list[int]:
        n = len(s)
        z = [0] * n
        # [L, R] represents the current bounding box of the rightmost prefix match
        L, R = 0, 0
        
        for i in range(1, n):
            # If i is within the bounding box, we can copy the previously calculated value
            if i <= R:
                z[i] = min(R - i + 1, z[i - L])
                
            # Manually expand the box if necessary
            while i + z[i] < n and s[z[i]] == s[i + z[i]]:
                z[i] += 1
                
            # If the new match extends past our current right bound, update the box
            if i + z[i] - 1 > R:
                L = i
                R = i + z[i] - 1
                
        return z

    @staticmethod
    def search(pattern: str, text: str) -> list[int]:
        matches = []
        if not pattern or not text:
            return matches

        # Concatenate pattern and text with a unique separator
        # Note: In a true ultra-low-memory environment, we would virtualize this!
        concat = pattern + "$" + text
        m = len(pattern)
        
        z_array = ZAlgorithm._get_z_array(concat)
        
        # Any Z-value exactly equal to the pattern length is a match
        for i in range(len(z_array)):
            if z_array[i] == m:
                # Calculate original index in the text: i - length(pattern) - length("$")
                matches.append(i - m - 1)
                
        return matches

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    text = "AABAACAADAABAABA"
    pattern = "AABA"
    
    results = ZAlgorithm.search(pattern, text)
    
    # "AABA" appears at indices 0, 9, and 12
    assert results == [0, 9, 12], f"Failed! Expected [0, 9, 12], got {results}"
    
    print("Python Z-Algorithm Pattern Matching Test Passed!")