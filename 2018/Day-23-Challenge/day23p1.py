import re
import os

def solve():
    # 1. Locate and parse input.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    if not os.path.exists(file_path):
        return "Error: input.txt not found."

    nanobots = []
    # Pattern to extract x, y, z, and r
    pattern = re.compile(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)")

    with open(file_path, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                x, y, z, r = map(int, match.groups())
                nanobots.append({'pos': (x, y, z), 'r': r})

    # 2. Find the nanobot with the largest radius
    # strongest will be the dict entry with the maximum 'r'
    strongest = max(nanobots, key=lambda n: n['r'])
    sx, sy, sz = strongest['pos']
    s_radius = strongest['r']

    # 3. Count nanobots in range of the strongest
    count_in_range = 0
    for bot in nanobots:
        bx, by, bz = bot['pos']
        # Calculate Manhattan distance
        distance = abs(sx - bx) + abs(sy - by) + abs(sz - bz)
        
        if distance <= s_radius:
            count_in_range += 1

    return count_in_range

if __name__ == "__main__":
    result = solve()
    print(f"Nanobots in range of the strongest: {result}")