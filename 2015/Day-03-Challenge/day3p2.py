import os

def solve_santa_puzzle(directions_file):
    """
    Simulates Santa's and Robo-Santa's paths on an infinite 2D grid, 
    taking alternating turns, and counts the total number of houses 
    that receive at least one present.
    """
    try:
        with open(directions_file, 'r') as f:
            # The input is expected to be a single continuous line of directions
            directions = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Directions file not found at '{directions_file}'")
        return 0
    
    # Santa and Robo-Santa start at (0, 0)
    santa_x, santa_y = 0, 0
    robo_x, robo_y = 0, 0
    
    # Set to store unique (x, y) coordinates of visited houses
    visited_houses = set()
    
    # Both deliver a present to the starting house
    visited_houses.add((0, 0))
    
    # Define movement vectors (dx, dy)
    move_map = {
        '^': (0, 1),   # North: Up Y
        'v': (0, -1),  # South: Down Y
        '>': (1, 0),   # East: Right X
        '<': (-1, 0)   # West: Left X
    }
    
    # Process each move, alternating between Santa and Robo-Santa
    for i, move in enumerate(directions):
        if move not in move_map:
            continue

        dx, dy = move_map[move]
        
        if i % 2 == 0:
            # Even index (0, 2, 4, ...): Santa's turn
            santa_x += dx
            santa_y += dy
            visited_houses.add((santa_x, santa_y))
        else:
            # Odd index (1, 3, 5, ...): Robo-Santa's turn
            robo_x += dx
            robo_y += dy
            visited_houses.add((robo_x, robo_y))
            
    # The score is the total number of unique houses visited
    return len(visited_houses)

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting Santa and Robo-Santa path simulation on: {os.path.abspath(input_file)}\n")
    
    final_score = solve_santa_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART TWO: TOTAL NUMBER OF HOUSES RECEIVING AT LEAST ONE PRESENT:")
    print(f"SCORE: {final_score}")
    print("="*50)