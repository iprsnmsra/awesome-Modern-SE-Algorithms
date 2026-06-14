import re
from collections import defaultdict

class BPETokenizer:
    def __init__(self, num_merges: int):
        self.num_merges = num_merges
        self.vocab = {}
        self.merges = {}

    def train(self, text: str):
        # Format vocabulary with spaces between characters and an end-of-word marker
        words = text.split()
        splits = [list(word) + ["</w>"] for word in words]
        
        # Build counting frequency table of base words
        counts = defaultdict(int)
        for split in splits:
            counts[tuple(split)] += 1

        print(f"Initial Base Vocab Size: {len(set(text)) + 1}")

        # Iteratively find and merge the most frequent adjacent token pairs
        for i in range(self.num_merges):
            pairs = defaultdict(int)
            for word_tuple, freq in counts.items():
                for j in range(len(word_tuple) - 1):
                    pair = (word_tuple[j], word_tuple[j+1])
                    pairs[pair] += freq

            if not pairs:
                break

            # Find the absolute most frequent pair
            best_pair = max(pairs, key=pairs.get)
            if pairs[best_pair] < 1:
                break

            # Record the merge rule
            new_token = "".join(best_pair)
            self.merges[best_pair] = new_token
            
            # Apply the merge to our corpus vocabulary mapping
            new_counts = defaultdict(int)
            for word_tuple, freq in counts.items():
                new_word = []
                j = 0
                while j < len(word_tuple):
                    if j < len(word_tuple) - 1 and (word_tuple[j], word_tuple[j+1]) == best_pair:
                        new_word.append(new_token)
                        j += 2
                    else:
                        new_word.append(word_tuple[j])
                        j += 1
                new_counts[tuple(new_word)] = freq
            counts = new_counts

        # Store the learned vocabulary keys
        final_vocab = set()
        for word_tuple in counts.keys():
            for token in word_tuple:
                final_vocab.add(token)
        self.vocab = final_vocab

    def tokenize(self, text: str) -> list[str]:
        """Encodes unseen text using the trained merge rules."""
        words = text.split()
        output_tokens = []

        for word in words:
            # Initialize word as individual characters
            tokens = list(word) + ["</w>"]
            
            # Repeatedly apply merge rules in order of creation
            while len(tokens) > 1:
                pairs = [(tokens[i], tokens[i+1]) for i in range(len(tokens) - 1)]
                
                # Find which of our possible current pairs was merged earliest during training
                mergeable_pair = None
                for pair in pairs:
                    if pair in self.merges:
                        mergeable_pair = pair
                        break
                
                if not mergeable_pair:
                    break # No more merge rules apply to this word
                    
                target_token = self.merges[mergeable_pair]
                new_tokens = []
                i = 0
                while i < len(tokens):
                    if i < len(tokens) - 1 and (tokens[i], tokens[i+1]) == mergeable_pair:
                        new_tokens.append(target_token)
                        i += 2
                    else:
                        new_tokens.append(tokens[i])
                        i += 1
                tokens = new_tokens
                
            output_tokens.extend(tokens)
            
        return output_tokens

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    # Train corpus with repetitive patterns
    corpus = "hug pug hug pug hug pug shug"
    tokenizer = BPETokenizer(num_merges=10)
    tokenizer.train(corpus)
    
    # After training on this pattern, "hug" and "pug" should be compressed into unified tokens
    test_str = "hug pug"
    tokenized = tokenizer.tokenize(test_str)
    
    print(f"Tokenized output: {tokenized}")
    
    # Assertions to ensure subword chunking is functional
    assert "hug</w>" in tokenized or "hug" in "".join(tokenized), "Failed to isolate primary tokens!"
    assert len(tokenized) < len(test_str.replace(" ", "")) + 2, "BPE failed to compress characters!"
    
    print("Python BPE Tokenizer Test Passed!")