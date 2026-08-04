import heapq
import re
import os

def solve():
    # 1. Dynamically locate the input file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    if not os.path.exists(file_path):
        return f"Error: Could not find 'input.txt' in {script_dir}"

    with open(file_path, 'r') as f:
        data = f.read()
    
    depth = int(re.search(r'depth: (\d+)', data).group(1))
    target_x, target_y = map(int, re.search(r'target: (\d+),(\d+)', data).groups())

    # Tool mapping: 0=Neither, 1=Torch, 2=Climbing Gear
    # Region mapping: 0=Rocky, 1=Wet, 2=Narrow
    valid_tools = {
        0: (1, 2), # Rocky: Torch (1) or Gear (2)
        1: (0, 2), # Wet: Neither (0) or Gear (2)
        2: (0, 1)  # Narrow: Neither (0) or Torch (1)
    }

    memo_erosion = {}

    def get_erosion(x, y):
        if (x, y) in memo_erosion:
            return memo_erosion[(x, y)]
        
        if (x, y) == (0, 0) or (x, y) == (target_x, target_y):
            geo = 0
        elif y == 0:
            geo = x * 16807
        elif x == 0:
            geo = y * 48271
        else:
            # GI depends on previously calculated erosion levels
            geo = get_erosion(x-1, y) * get_erosion(x, y-1)
            
        erosion = (geo + depth) % 20183
        memo_erosion[(x, y)] = erosion
        return erosion

    def get_type(x, y):
        return get_erosion(x, y) % 3

    # Priority Queue: (minutes, x, y, tool)
    pq = [(0, 0, 0, 1)] # Start at (0,0) with Torch
    visited = {}

    

    while pq:
        minutes, x, y, tool = heapq.heappop(pq)
        
        state = (x, y, tool)
        if visited.get(state, float('inf')) <= minutes:
            continue
        visited[state] = minutes
        
        # Check if we reached the goal
        if x == target_x and y == target_y:
            if tool == 1:
                return minutes
            else:
                # Must switch to torch at target (7 minutes)
                heapq.heappush(pq, (minutes + 7, x, y, 1))
                continue

        # Option A: Switch tools (7 min)
        region_type = get_type(x, y)
        for next_tool in valid_tools[region_type]:
            if next_tool != tool:
                heapq.heappush(pq, (minutes + 7, x, y, next_tool))

        # Option B: Move to adjacent region (1 min)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if nx < 0 or ny < 0:
                continue
            
            # Allow searching up to 100 units past the target
            if nx > target_x + 100 or ny > target_y + 100:
                continue
            
            next_region_type = get_type(nx, ny)
            if tool in valid_tools[next_region_type]:
                heapq.heappush(pq, (minutes + 1, nx, ny, tool))

if __name__ == "__main__":
    print(f"Fewest minutes to reach the target: {solve()}")