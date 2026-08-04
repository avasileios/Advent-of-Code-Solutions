import os
from collections import defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def solve_chronal_coordinates(path):
    coords = []
    with open(path, 'r') as f:
        for line in f:
            x, y = map(int, line.strip().split(', '))
            coords.append((x, y))

    # Determine bounding box
    min_x = min(c[0] for c in coords)
    max_x = max(c[0] for c in coords)
    min_y = min(c[1] for c in coords)
    max_y = max(c[1] for c in coords)

    area_counts = defaultdict(int)
    infinite_ids = set()

    # Iterate through the bounding box
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            distances = []
            for i, (cx, cy) in enumerate(coords):
                dist = abs(x - cx) + abs(y - cy)
                distances.append((dist, i))
            
            distances.sort()
            
            # Check if there's a unique closest point
            if distances[0][0] < distances[1][0]:
                closest_id = distances[0][1]
                area_counts[closest_id] += 1
                
                # If this point is on the edge, the area is infinite
                if x == min_x or x == max_x or y == min_y or y == max_y:
                    infinite_ids.add(closest_id)

    # Filter out infinite areas and find the max
    finite_areas = [area_counts[cid] for cid in area_counts if cid not in infinite_ids]
    
    return max(finite_areas)

if __name__ == "__main__":
    result = solve_chronal_coordinates(file_path)
    print(f"The size of the largest finite area is: {result}")