import os

def solve_long_term(target_minutes=1000000000):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    
    with open(file_path, 'r') as f:
        grid = tuple(line.strip() for line in f if line.strip())

    history = {}
    history[grid] = 0
    
    minute = 0
    while minute < target_minutes:
        minute += 1
        new_grid = []
        for r in range(len(grid)):
            new_row = []
            for c in range(len(grid[0])):
                trees = 0
                lumberyards = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0: continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                            char = grid[nr][nc]
                            if char == '|': trees += 1
                            elif char == '#': lumberyards += 1
                
                curr = grid[r][c]
                if curr == '.' and trees >= 3: res = '|'
                elif curr == '|' and lumberyards >= 3: res = '#'
                elif curr == '#':
                    res = '#' if (lumberyards >= 1 and trees >= 1) else '.'
                else: res = curr
                new_row.append(res)
            new_grid.append("".join(new_row))
        
        grid = tuple(new_grid)
        
        # Cycle Detection
        if grid in history:
            prev_minute = history[grid]
            cycle_len = minute - prev_minute
            remaining = target_minutes - minute
            # Skip ahead
            offset = remaining % cycle_len
            # We only need to simulate 'offset' more minutes
            for _ in range(offset):
                grid = simulate_one_step(grid)
            break
        
        history[grid] = minute

    wooded = "".join(grid).count('|')
    lumber = "".join(grid).count('#')
    return wooded * lumber

def simulate_one_step(grid):
    rows, cols = len(grid), len(grid[0])
    new_grid = []
    for r in range(rows):
        new_row = []
        for c in range(cols):
            t, l = 0, 0
            for dr in [-1,0,1]:
                for dc in [-1,0,1]:
                    if dr == 0 and dc == 0: continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == '|': t += 1
                        elif grid[nr][nc] == '#': l += 1
            curr = grid[r][c]
            if curr == '.' and t >= 3: res = '|'
            elif curr == '|' and l >= 3: res = '#'
            elif curr == '#': res = '#' if (l >= 1 and t >= 1) else '.'
            else: res = curr
            new_row.append(res)
        new_grid.append("".join(new_row))
    return tuple(new_grid)

if __name__ == "__main__":
    print(f"Total resource value after 1,000,000,000 minutes: {solve_long_term()}")