import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def solve_safe_region(path, threshold=10000):
    coords = []
    with open(path, 'r') as f:
        for line in f:
            if line.strip():
                x, y = map(int, line.strip().split(', '))
                coords.append((x, y))

    # Bounding box
    min_x = min(c[0] for c in coords)
    max_x = max(c[0] for c in coords)
    min_y = min(c[1] for c in coords)
    max_y = max(c[1] for c in coords)

    region_size = 0

    # Iterate through the grid
    # Note: If your threshold is very large, you might need to expand 
    # the range slightly, but for 10,000, the bounding box is usually safe.
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            total_dist = 0
            for cx, cy in coords:
                total_dist += abs(x - cx) + abs(y - cy)
            
            if total_dist < threshold:
                region_size += 1
                
    return region_size

if __name__ == "__main__":
    # The puzzle specifies a threshold of 10,000
    result = solve_safe_region(file_path, 10000)
    print(f"The size of the safe region is: {result}")