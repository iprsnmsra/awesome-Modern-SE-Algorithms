import heapq

class AStar:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def heuristic(self, a, b):
        # Manhattan distance on a square grid
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_path(self, start, goal):
        # Priority Queue stores: (f_cost, current_node)
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        came_from = {}
        
        # g_score: Cost from start to node
        g_score = {start: 0}
        
        # f_score: g_score + heuristic
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            current_f, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1] # Reverse to get Start -> Goal

            # Check 4 adjacent neighbors (Up, Down, Left, Right)
            neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            for dx, dy in neighbors:
                neighbor = (current[0] + dx, current[1] + dy)
                
                # Check bounds and walls (0 = free space, 1 = wall)
                if 0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.cols:
                    if self.grid[neighbor[0]][neighbor[1]] == 1:
                        continue

                    tentative_g_score = g_score[current] + 1

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                        
                        # Only push if we found a strictly better path
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return [] # No path found

# --- CI/CD Automated Test ---
if __name__ == '__main__':
    # 0 = Path, 1 = Wall
    maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    
    astar = AStar(maze)
    start_node = (0, 0)
    end_node = (4, 4)
    
    path = astar.find_path(start_node, end_node)
    
    # Path should successfully navigate around the '1's
    assert len(path) > 0, "A* failed to find a path!"
    assert path[0] == start_node, "Path doesn't begin at start."
    assert path[-1] == end_node, "Path doesn't arrive at goal."
    
    print(f"Python A* Pathfinding Test Passed! Path length: {len(path)}")