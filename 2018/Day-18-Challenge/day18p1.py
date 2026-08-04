import os

def solve():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    with open(file_path, 'r') as f:
        grid = [line.strip() for line in f if line.strip()]

    rows = len(grid)
    cols = len(grid[0])

    # Simulation for 10 minutes
    for minute in range(10):
        new_grid = []
        for r in range(rows):
            new_row = ""
            for c in range(cols):
                # Count neighbors
                trees = 0
                lumberyards = 0
                
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            char = grid[nr][nc]
                            if char == '|':
                                trees += 1
                            elif char == '#':
                                lumberyards += 1
                
                # Apply rules
                current = grid[r][c]
                if current == '.' and trees >= 3:
                    new_row += '|'
                elif current == '|' and lumberyards >= 3:
                    new_row += '#'
                elif current == '#':
                    if lumberyards >= 1 and trees >= 1:
                        new_row += '#'
                    else:
                        new_row += '.'
                else:
                    new_row += current
            new_grid.append(new_row)
        grid = new_grid

    # Calculate total resource value
    all_acres = "".join(grid)
    wooded = all_acres.count('|')
    lumber = all_acres.count('#')
    
    return wooded * lumber

if __name__ == "__main__":
    result = solve()
    print(f"Total resource value after 10 minutes: {result}")