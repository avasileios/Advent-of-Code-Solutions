import sys
import re
import os

# Increase recursion depth for deep cavern systems
sys.setrecursionlimit(10000)

def solve():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    clay = set()
    min_y, max_y = float('inf'), float('-inf')

    # --- 1. Parsing the Scan Data ---
    try:
        with open(file_path, 'r') as f:
            for line in f:
                coords = {m[0]: list(map(int, m[1].split('..'))) if '..' in m[1] else [int(m[1])] 
                          for m in re.findall(r'([xy])=([\d\.]+)', line)}
                
                x_range = coords['x'] if len(coords['x']) > 1 else [coords['x'][0], coords['x'][0]]
                y_range = coords['y'] if len(coords['y']) > 1 else [coords['y'][0], coords['y'][0]]
                
                for x in range(x_range[0], x_range[1] + 1):
                    for y in range(y_range[0], y_range[1] + 1):
                        clay.add((x, y))
                        min_y = min(min_y, y)
                        max_y = max(max_y, y)
    except FileNotFoundError:
        return "Error: input.txt not found."

    settled = set()
    flowing = set()

    # --- 2. Water Flow Logic ---
    def fill(x, y):
        if y > max_y:
            return
        if (x, y) in clay or (x, y) in settled:
            return

        flowing.add((x, y))

        # Fall Down
        below = (x, y + 1)
        if below not in clay and below not in settled:
            fill(x, y + 1)
        
        # If no floor below, we can't spread
        if below not in clay and below not in settled:
            return

        # Spread Horizontally
        left_x, left_blocked = spread(x, y, -1)
        right_x, right_blocked = spread(x, y, 1)

        if left_blocked and right_blocked:
            # Basin is contained on both sides
            for ix in range(left_x, right_x + 1):
                settled.add((ix, y))
                if (ix, y) in flowing:
                    flowing.remove((ix, y))
        else:
            # Water spills out one or both sides
            for ix in range(left_x, right_x + 1):
                flowing.add((ix, y))

    def spread(x, y, dx):
        curr_x = x
        while True:
            below = (curr_x, y + 1)
            if below not in clay and below not in settled:
                fill(curr_x, y)
                return curr_x, False
            
            next_x = curr_x + dx
            if (next_x, y) in clay:
                return curr_x, True
            
            curr_x = next_x

    # --- 3. Run Simulation ---
    fill(500, 0)

    # --- 4. Filtering by Y-range ---
    total_reached = sum(1 for x, y in (settled | flowing) if min_y <= y <= max_y)
    total_retained = sum(1 for x, y in settled if min_y <= y <= max_y)

    return total_reached, total_retained

if __name__ == "__main__":
    p1, p2 = solve()
    print(f"Part 1 (Total reached): {p1}")
    print(f"Part 2 (Water retained): {p2}")