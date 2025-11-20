import os
import re
from collections import deque

# --- Constants ---
GRID_W = 35
GRID_H = 25
# Goal starts at top-right
GOAL_START = (GRID_W - 1, 0) # (34, 0)
# Target for empty slot is to the left of the goal
TARGET_FOR_EMPTY = (GOAL_START[0] - 1, GOAL_START[1]) # (33, 0)

def parse_grid(filepath):
    """
    Parses the input to find the empty node and identify wall locations.
    """
    walls = set()
    empty_pos = None
    
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Input file not found at {filepath}")
        return None, None

    # Regex for: /dev/grid/node-x0-y0     94T   65T    29T   69%
    pattern = re.compile(r'node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T')
    
    for line in lines:
        match = pattern.search(line)
        if match:
            x = int(match.group(1))
            y = int(match.group(2))
            size = int(match.group(3))
            used = int(match.group(4))
            
            # 1. Identify Empty Slot
            if used == 0:
                empty_pos = (x, y)
            
            # 2. Identify Walls
            # In this puzzle, "Walls" are nodes with huge data (Used > 100T)
            # that simply cannot be moved into smaller nodes (~90T).
            if used > 100:
                walls.add((x, y))
                
    return empty_pos, walls

def solve_bfs_empty_to_target(start_pos, target_pos, walls):
    """
    BFS to find the shortest path for the empty slot to reach the target.
    Note: The Empty Slot cannot move into a Wall.
    It also cannot move into the Goal Data (G) at (34, 0) during this phase.
    """
    queue = deque([(start_pos, 0)])
    visited = {start_pos}
    
    # We must avoid the Goal Data's current position during Phase 1
    # effectively treating it as a wall for the empty slot.
    obstacles = walls.copy()
    obstacles.add(GOAL_START)
    
    while queue:
        (x, y), steps = queue.popleft()
        
        if (x, y) == target_pos:
            return steps
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < GRID_W and 0 <= ny < GRID_H:
                if (nx, ny) not in obstacles and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), steps + 1))
                    
    return -1 # Should not happen

def solve_puzzle(filepath):
    empty_pos, walls = parse_grid(filepath)
    
    if not empty_pos:
        return 0
        
    print(f"Empty Slot Start: {empty_pos}")
    print(f"Goal Data Start: {GOAL_START}")
    print(f"Wall Count: {len(walls)}")
    
    # --- Phase 1: Move Empty Slot to Neighbor of Goal ---
    # Target: (33, 0)
    steps_phase_1 = solve_bfs_empty_to_target(empty_pos, TARGET_FOR_EMPTY, walls)
    
    if steps_phase_1 == -1:
        print("Error: Could not reach target.")
        return 0
        
    print(f"Phase 1 Steps (Reach Goal Neighbor): {steps_phase_1}")
    
    # --- Phase 2: Move Goal to (0, 0) ---
    # 1. Initial Swap: Empty (33,0) <-> Goal (34,0). Goal moves to (33,0). Cost: 1.
    #    Empty slot is now at (34,0).
    # 2. Cycling: We need to move Goal from (33,0) to (0,0). Distance = 33.
    #    Each step requires 5 moves (Empty circles around: Down, Left, Left, Up, Right-Swap).
    
    # Distance for G to travel after first swap: 33
    # Cost per step: 5
    
    # Total Phase 2 = 1 (Initial Swap) + (Distance - 1) * 5
    # Wait, let's trace carefully.
    # G is at x=34. We want G at x=0. Total 34 steps.
    # Step 1: Swap. Cost 1. G at 33. Empty at 34.
    # Remaining G steps: 33.
    # To move G from x to x-1:
    #   Empty is at x+1.
    #   Empty path: (x+1, 1) -> (x, 1) -> (x-1, 1) -> (x-1, 0). (4 steps)
    #   Swap: (x-1, 0) with (x, 0). (1 step).
    #   Total 5 steps per shift.
    
    steps_phase_2 = 1 + (33 * 5)
    
    total_steps = steps_phase_1 + steps_phase_2
    
    return total_steps

if __name__ == "__main__":
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    print(f"Solving for input: {os.path.abspath(input_file)}")
    result = solve_puzzle(input_file)
    print("\n" + "="*50)
    print(f"FEWEST NUMBER OF STEPS: {result}")
    print("="*50)