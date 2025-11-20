import os

def solve_santa_puzzle(directions_file):
    """
    Simulates Santa's path on an infinite 2D grid and counts the number of 
    houses that receive at least one present.
    """
    try:
        with open(directions_file, 'r') as f:
            # The input is expected to be a single continuous line of directions
            directions = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Directions file not found at '{directions_file}'")
        return 0
    
    # Santa starts at (0, 0)
    current_x = 0
    current_y = 0
    
    # Set to store unique (x, y) coordinates of visited houses
    visited_houses = set()
    
    # Add the starting house
    visited_houses.add((current_x, current_y))
    
    # Define movement vectors (dx, dy)
    move_map = {
        '^': (0, 1),   # North: Up Y
        'v': (0, -1),  # South: Down Y
        '>': (1, 0),   # East: Right X
        '<': (-1, 0)   # West: Left X
    }
    
    # Process each move
    for move in directions:
        if move in move_map:
            dx, dy = move_map[move]
            
            # Update Santa's position
            current_x += dx
            current_y += dy
            
            # Deliver a present by adding the new house to the set
            visited_houses.add((current_x, current_y))
            
    # The score is the total number of unique houses visited
    return len(visited_houses)

# --- Main Execution Block ---
if __name__ == "__main__":
    input_file= os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    print(f"Starting Santa's path simulation on: {os.path.abspath(input_file)}\n")
    
    final_score = solve_santa_puzzle(input_file)
    
    print("\n" + "="*50)
    print("TOTAL NUMBER OF HOUSES RECEIVING AT LEAST ONE PRESENT:")
    print(f"SCORE: {final_score}")
    print("="*50)