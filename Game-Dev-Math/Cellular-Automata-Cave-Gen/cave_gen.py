import random

class CaveGenerator:
    def __init__(self, width: int, height: int, fill_probability: float = 0.45):
        self.width = width
        self.height = height
        self.fill_probability = fill_probability
        self.map = self._generate_random_map()

    def _generate_random_map(self) -> list[list[int]]:
        # 1 = Wall, 0 = Air
        grid = []
        for x in range(self.width):
            row = []
            for y in range(self.height):
                # Force outer edges to be walls to enclose the map
                if x == 0 or x == self.width - 1 or y == 0 or y == self.height - 1:
                    row.append(1)
                else:
                    row.append(1 if random.random() < self.fill_probability else 0)
            grid.append(row)
        return grid

    def _get_surrounding_wall_count(self, grid: list[list[int]], grid_x: int, grid_y: int) -> int:
        wall_count = 0
        for neighbor_x in range(grid_x - 1, grid_x + 2):
            for neighbor_y in range(grid_y - 1, grid_y + 2):
                if neighbor_x >= 0 and neighbor_x < self.width and neighbor_y >= 0 and neighbor_y < self.height:
                    if neighbor_x != grid_x or neighbor_y != grid_y:
                        wall_count += grid[neighbor_x][neighbor_y]
                else:
                    wall_count += 1 # Edges count as walls
        return wall_count

    def smooth_map(self):
        new_map = [[0 for _ in range(self.height)] for _ in range(self.width)]
        
        for x in range(self.width):
            for y in range(self.height):
                neighbor_walls = self._get_surrounding_wall_count(self.map, x, y)
                
                # The Cellular Automata Rules
                if neighbor_walls > 4:
                    new_map[x][y] = 1
                elif neighbor_walls < 4:
                    new_map[x][y] = 0
                else:
                    new_map[x][y] = self.map[x][y] # Tie: Keep original state
                    
        self.map = new_map

    def print_map(self):
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                line += "# " if self.map[x][y] == 1 else ". "
            print(line)

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    cave = CaveGenerator(width=30, height=15, fill_probability=0.45)
    
    # Run the simulation 5 times to erode the noise into smooth caves
    for _ in range(5):
        cave.smooth_map()
        
    cave.print_map()
    
    # Verify the outer walls are solid
    assert cave.map[0][0] == 1, "Outer walls failed to generate!"
    
    print("\nPython Cellular Automata Cave Gen Test Passed!")