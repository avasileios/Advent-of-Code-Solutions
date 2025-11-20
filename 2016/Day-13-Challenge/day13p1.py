import os
from collections import deque
import sys

# Set a reasonable limit for the search area (since the maze is technically infinite)
MAX_DIM = 50 

# Directions: (dx, dy)
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)] 

# Office designer's favorite number (puzzle input)
FAVORITE_NUMBER = 1358

# Target coordinates
START_POS = (1, 1)
END_POS = (31, 39)

def is_open_space(x: int, y: int) -> bool:
    """
    Determines if the coordinate (x, y) is an open space or a wall.
    
    Rule: Even number of set bits (1s) in the binary representation of the sum.
    """
    if x < 0 or y < 0:
        return False # Invalid negative coordinates are outside the building/walls

    # 1. Calculate the value
    value = x*x + 3*x + 2*x*y + y + y*y
    
    # 2. Add the favorite number
    sum_val = value + FAVORITE_NUMBER
    
    # 3. Count the number of set bits (1s) in the binary representation
    # bin(sum_val).count('1') is the most efficient way to get the population count.
    set_bits = bin(sum_val).count('1')
    
    # 4. Check rule: Even count of set bits is an open space.
    return set_bits % 2 == 0

def find_shortest_path():
    """
    Performs BFS to find the minimum number of steps from START_POS to END_POS.
    """
    # Queue stores: (x, y, distance)
    queue = deque([(START_POS[0], START_POS[1], 0)]) 
    # Visited set stores: (x, y) to prevent loops
    visited = set([START_POS])
    
    # Max size estimation based on END_POS
    max_search_dim = max(END_POS) + 5 

    while queue:
        x, y, dist = queue.popleft()
        
        if (x, y) == END_POS:
            return dist
            
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            next_pos = (nx, ny)
            
            # 1. Check validity: non-negative coordinates
            if nx < 0 or ny < 0:
                continue
            
            # 2. Check if the next space is a wall AND is unvisited
            if next_pos not in visited and is_open_space(nx, ny):
                visited.add(next_pos)
                queue.append((nx, ny, dist + 1))
                
    return -1 # Path not found

def visualize_maze_path(path_coords, size):
    """
    Helper function to visualize the maze and the path (not used in main solver).
    """
    grid = []
    for y in range(size):
        row = ""
        for x in range(size):
            if x == START_POS[0] and y == START_POS[1]:
                char = 'S'
            elif x == END_POS[0] and y == END_POS[1]:
                char = 'E'
            elif (x, y) in path_coords:
                char = 'O'
            elif is_open_space(x, y):
                char = '.'
            else:
                char = '#'
            row += char
        grid.append(row)
    return "\n".join(grid)


# --- Main Execution Block ---
if __name__ == "__main__":
    
    print(f"Office Designer's Favorite Number: {FAVORITE_NUMBER}")
    print(f"Target: {END_POS}. Starting at: {START_POS}.")
    
    final_steps = find_shortest_path()
    
    print("\n" + "="*50)
    print("FEWEST NUMBER OF STEPS REQUIRED TO REACH TARGET:")
    print(f"SCORE: {final_steps}")
    print("="*50)

