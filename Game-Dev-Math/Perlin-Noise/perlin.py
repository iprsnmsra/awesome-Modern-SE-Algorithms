import math

class PerlinNoise:
    def __init__(self):
        # The standard 256 Permutation Table
        p = [151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,142,8,99,37,240,21,10,23,
             190, 6,148,247,120,234,75,0,26,197,62,94,252,219,203,117,35,11,32,57,177,33,88,237,149,56,87,174,20,125,136,171,168, 68,175,74,165,71,134,139,48,27,166,
             77,146,158,231,83,111,229,122,60,211,133,230,220,105,92,41,55,46,245,40,244,102,143,54, 65,25,63,161, 1,216,80,73,209,76,132,187,208, 89,18,169,200,196,
             135,130,116,188,159,86,164,100,109,198,173,186, 3,64,52,217,226,250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,47,16,58,17,182,189,28,42,
             223,183,170,213,119,248,152, 2,44,154,163, 70,221,153,101,155,167, 43,172,9,129,22,39,253, 19,98,108,110,79,113,224,232,178,185, 112,104,218,246,97,228,
             251,34,242,193,238,210,144,12,191,179,162,241, 81,51,145,235,249,14,239,107,49,192,214, 31,181,199,106,157,184, 84,204,176,115,121,50,45,127, 4,150,254,
             138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,156,180]
        # Duplicate the array to avoid overflow wrapping in math
        self.p = p + p

    def fade(self, t):
        # 6t^5 - 15t^4 + 10t^3 (The magic smoothing curve)
        return t * t * t * (t * (t * 6 - 15) + 10)

    def lerp(self, t, a, b):
        return a + t * (b - a)

    def grad(self, hash, x, y):
        h = hash & 15
        u = x if h < 8 else y
        v = y if h < 4 else (x if h == 12 or h == 14 else 0)
        return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)

    def noise(self, x, y):
        X = int(math.floor(x)) & 255
        Y = int(math.floor(y)) & 255

        x -= math.floor(x)
        y -= math.floor(y)

        u = self.fade(x)
        v = self.fade(y)

        A = self.p[X] + Y
        B = self.p[X + 1] + Y

        return self.lerp(v, self.lerp(u, self.grad(self.p[A], x, y), self.grad(self.p[B], x - 1, y)),
                         self.lerp(u, self.grad(self.p[A + 1], x, y - 1), self.grad(self.p[B + 1], x - 1, y - 1)))

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    generator = PerlinNoise()
    
    # Check two coordinates very close to each other
    val1 = generator.noise(10.1, 10.1)
    val2 = generator.noise(10.11, 10.1)
    
    # In procedural terrain, close coordinates MUST have close heights (organic smoothness)
    diff = abs(val1 - val2)
    
    assert diff < 0.1, f"Noise jump was too harsh! Expected < 0.1, got {diff}"
    print(f"Python Perlin Noise Test Passed! (Organic transition difference: {diff:.4f})")