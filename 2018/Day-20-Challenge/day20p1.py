import os

def solve():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')

    with open(file_path, 'r') as f:
        regex = f.read().strip()

    # Distances from (0,0) to each room (x, y)
    distances = {(0, 0): 0}
    # Stack to keep track of positions before branches '('
    stack = []
    
    curr_x, curr_y = 0, 0
    
    # Mapping directions to coordinate changes
    moves = {
        'N': (0, 1),
        'S': (0, -1),
        'E': (1, 0),
        'W': (-1, 0)
    }

    for char in regex:
        if char == '^' or char == '$':
            continue
        elif char == '(':
            # Start of a branch: save current position
            stack.append((curr_x, curr_y))
        elif char == ')':
            # End of a branch: go back to the start of the branch
            curr_x, curr_y = stack.pop()
        elif char == '|':
            # Another option in the branch: reset to the saved position
            curr_x, curr_y = stack[-1]
        else:
            # Moving to a new room
            dx, dy = moves[char]
            prev_dist = distances[(curr_x, curr_y)]
            curr_x += dx
            curr_y += dy
            
            # If the room is new or we found a shorter path, update it
            if (curr_x, curr_y) not in distances or distances[(curr_x, curr_y)] > prev_dist + 1:
                distances[(curr_x, curr_y)] = prev_dist + 1

    # The answer to Part 1 is the maximum distance found
    return max(distances.values())

if __name__ == "__main__":
    result = solve()
    print(f"The furthest room is {result} doors away.")