import os

# Directions mapping (x, y)
# Note: In grid (row, col), x is col, y is row.
DIRS = {
    "n": (0, -1), # Up
    "e": (1, 0),  # Right
    "s": (0, 1),  # Down
    "w": (-1, 0)  # Left
}

# Opposite directions to prevent 180 turns
ANTI = {"n": "s", "e": "w", "s": "n", "w": "e"}

def parse_diagram(filepath):
    """
    Reads the diagram into a rectangular list of strings (grid), padding shorter 
    rows with spaces to prevent IndexError.
    """
    try:
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            # Read all lines, removing newlines but keeping internal spaces
            lines = [line.rstrip('\r\n').expandtabs(8) for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'")
        return []

    if not lines:
        return []

    # Pad rows to max width
    max_width = max(len(line) for line in lines)
    grid = [line.ljust(max_width) for line in lines]
    
    return grid

def find_start(grid):
    """Finds the starting '|' in the top row."""
    y = 0
    try:
        x = grid[y].index('|')
        return (x, y)
    except ValueError:
        return None

def solve_packet_tracer(filepath):
    """
    Simulates the packet path using the user's optimized logic.
    Returns (letters_collected, total_steps).
    """
    grid = parse_diagram(filepath)
    if not grid:
        return "", 0

    start_pos = find_start(grid)
    if not start_pos:
        return "", 0

    x, y = start_pos
    d = 's' # Start facing South
    ans = []
    steps = 0
    
    height = len(grid)
    width = len(grid[0])

    # Loop until we hit an empty space
    while 0 <= y < height and 0 <= x < width and grid[y][x] != ' ':
        
        steps += 1
        char = grid[y][x]
        
        # 1. Collect Letters
        if char not in "-|+":
            ans.append(char)

        # 2. Handle Turns (+)
        if char == '+':
            # Check possible next directions (excluding reverse)
            for nd in "nesw":
                if nd == ANTI[d]:
                    continue

                dx, dy = DIRS[nd]
                nx, ny = x + dx, y + dy
                
                # Check bounds and if the neighbor is not empty
                if 0 <= ny < height and 0 <= nx < width and grid[ny][nx] != ' ':
                    d = nd
                    break
        
        # 3. Move
        dx, dy = DIRS[d]
        x += dx
        y += dy

    return "".join(ans), steps

# --- Main Execution Block ---
if __name__ == "__main__":
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting packet path tracing using data from: {os.path.abspath(input_file)}\n")
    
    final_letters, total_steps = solve_packet_tracer(input_file)
    
    print("\n" + "="*50)
    print("PART 1: LETTERS SEEN ALONG THE PATH:")
    print(f"SCORE: {final_letters}")
    print("-" * 50)
    print("PART 2: TOTAL NUMBER OF STEPS TAKEN:")
    print(f"SCORE: {total_steps}")
    print("="*50)