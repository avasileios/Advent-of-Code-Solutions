import re
import os

def solve():
    # 1. Parse input.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    depth = int(re.search(r'depth: (\d+)', content).group(1))
    target_match = re.search(r'target: (\d+),(\d+)', content)
    target_x = int(target_match.group(1))
    target_y = int(target_match.group(2))

    # 2. Build the erosion level map
    # Using a dictionary for memoization
    erosion_levels = {}

    def get_erosion(x, y):
        if (x, y) in erosion_levels:
            return erosion_levels[(x, y)]
        
        if (x, y) == (0, 0) or (x, y) == (target_x, target_y):
            geo_index = 0
        elif y == 0:
            geo_index = x * 16807
        elif x == 0:
            geo_index = y * 48271
        else:
            # GI depends on previously calculated erosion levels
            geo_index = get_erosion(x - 1, y) * get_erosion(x, y - 1)
        
        erosion = (geo_index + depth) % 20183
        erosion_levels[(x, y)] = erosion
        return erosion

    # 3. Calculate total risk level
    total_risk = 0
    for y in range(target_y + 1):
        for x in range(target_x + 1):
            # Risk Level is Erosion Level % 3
            # 0: rocky, 1: wet, 2: narrow
            total_risk += get_erosion(x, y) % 3

    return total_risk

if __name__ == "__main__":
    print(f"Total risk level: {solve()}")