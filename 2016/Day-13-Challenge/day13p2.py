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
# Note: END_POS is irrelevant for this problem, but kept for context.
END_POS = (31, 39) 

# Part Two Constraint
MAX_STEPS = 50

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

def count_reachable_locations(max_steps: int) -> int:
    """
    Performs BFS to count the number of distinct (x, y) coordinates 
    reachable in at most max_steps from START_POS.
    """
    # Queue stores: (x, y, distance)
    queue = deque([(START_POS[0], START_POS[1], 0)]) 
    # Visited set stores: (x, y) coordinates
    visited = set([START_POS])
    
    # We do not need a dimension limit since the max_steps constraint will handle termination.

    while queue:
        x, y, dist = queue.popleft()
        
        # Optimization: If we already exceeded the maximum steps, we don't explore 
        # neighbors from this node, but we DO count the node itself if it was 
        # added with a distance <= max_steps.
        if dist >= max_steps:
            # We don't continue the search from here, but the node (x, y) itself 
            # is part of the visited count if dist == max_steps.
            continue
            
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            next_pos = (nx, ny)
            
            # 1. Check validity: non-negative coordinates
            if nx < 0 or ny < 0:
                continue
            
            # 2. Check if the next space is a wall AND is unvisited
            if next_pos not in visited and is_open_space(nx, ny):
                # Only enqueue if the next step is within the limit
                if dist + 1 <= max_steps:
                    visited.add(next_pos)
                    queue.append((nx, ny, dist + 1))
                
    # The score is the total count of unique visited locations
    return len(visited)

# --- Main Execution Block ---
if __name__ == "__main__":
    
    print(f"Office Designer's Favorite Number: {FAVORITE_NUMBER}")
    print(f"Target: Reachable area in at most {MAX_STEPS} steps.")
    
    final_count = count_reachable_locations(MAX_STEPS)
    
    print("\n" + "="*50)
    print(f"TOTAL DISTINCT LOCATIONS REACHABLE IN AT MOST {MAX_STEPS} STEPS:")
    print(f"SCORE: {final_count}")
    print("="*50)