import os

def solve():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')

    with open(file_path, 'r') as f:
        regex = f.read().strip()

    distances = {(0, 0): 0}
    stack = []
    curr_x, curr_y = 0, 0
    moves = {'N': (0, 1), 'S': (0, -1), 'E': (1, 0), 'W': (-1, 0)}

    for char in regex:
        if char == '^' or char == '$':
            continue
        elif char == '(':
            stack.append((curr_x, curr_y))
        elif char == ')':
            curr_x, curr_y = stack.pop()
        elif char == '|':
            curr_x, curr_y = stack[-1]
        else:
            dx, dy = moves[char]
            prev_dist = distances[(curr_x, curr_y)]
            curr_x += dx
            curr_y += dy
            
            # Record shortest distance to this room
            if (curr_x, curr_y) not in distances or distances[(curr_x, curr_y)] > prev_dist + 1:
                distances[(curr_x, curr_y)] = prev_dist + 1

    # Part 1: Furthest room
    part1 = max(distances.values())
    
    # Part 2: Rooms at least 1000 doors away
    part2 = sum(1 for d in distances.values() if d >= 1000)
    
    return part1, part2

if __name__ == "__main__":
    p1, p2 = solve()
    print(f"Part 1: The furthest room is {p1} doors away.")
    print(f"Part 2: There are {p2} rooms at least 1000 doors away.")