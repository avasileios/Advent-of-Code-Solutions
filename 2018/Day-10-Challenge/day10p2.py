import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def solve_stars():
    points = []
    with open(file_path, 'r') as f:
        for line in f:
            # Extract x, y, vx, vy
            nums = list(map(int, re.findall(r'-?\d+', line)))
            points.append(nums)

    prev_height = float('inf')
    t = 0

    while True:
        # Calculate current bounds
        min_x = min(x + vx * t for x, y, vx, vy in points)
        max_x = max(x + vx * t for x, y, vx, vy in points)
        min_y = min(y + vy * t for x, y, vx, vy in points)
        max_y = max(y + vy * t for x, y, vx, vy in points)

        current_height = max_y - min_y

        # If the box is starting to grow, the previous second was the message
        if current_height > prev_height:
            t -= 1 # Step back to the minimum
            break
        
        prev_height = current_height
        t += 1

    # Re-calculate final positions at the golden second
    final_points = set()
    min_x = min(x + vx * t for x, y, vx, vy in points)
    max_x = max(x + vx * t for x, y, vx, vy in points)
    min_y = min(y + vy * t for x, y, vx, vy in points)
    max_y = max(y + vy * t for x, y, vx, vy in points)

    for x, y, vx, vy in points:
        final_points.add((x + vx * t, y + vy * t))

    # Print the message
    print(f"Message found at T = {t} seconds:\n")

if __name__ == "__main__":
    solve_stars()