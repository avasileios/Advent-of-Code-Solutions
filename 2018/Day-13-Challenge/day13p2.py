import os

# --- Path Setup ---
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

class Cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.intersection_count = 0  # 0=Left, 1=Straight, 2=Right
        self.crashed = False
        self.id = f"{x},{y}" # Unique ID for debugging

    def __repr__(self):
        return f"Cart({self.x}, {self.y}, {self.direction})"

def solve():
    if not os.path.exists(file_path):
        print("Error: input.txt not found")
        return

    # 1. Parse and Pad Grid
    with open(file_path, 'r') as f:
        # Use simple newline stripping to preserve trailing spaces
        raw_lines = [line.strip('\n') for line in f.readlines()]

    max_width = max(len(line) for line in raw_lines)
    grid = []
    carts = []

    for y, line in enumerate(raw_lines):
        # Pad line to max_width
        padded_line = line.ljust(max_width)
        row = []
        for x, char in enumerate(padded_line):
            if char in '^v<>':
                # Create Cart
                carts.append(Cart(x, y, char))
                # The track under a cart is always a straight path matching direction
                if char in '^v':
                    row.append('|')
                else:
                    row.append('-')
            else:
                row.append(char)
        grid.append(row)

    print(f"Loaded Map: {max_width}x{len(grid)} with {len(carts)} carts.")

    # 2. Simulation Loop
    tick = 0
    while len(carts) > 1:
        tick += 1
        # Sort by Y, then X (Top-to-bottom, Left-to-right)
        carts.sort(key=lambda c: (c.y, c.x))
        
        # Position Lookup for fast collision detection
        # We rebuild this logic carefully to handle the "instant removal" rule
        cart_locations = {}
        for c in carts:
            if not c.crashed:
                cart_locations[(c.x, c.y)] = c

        for cart in carts:
            if cart.crashed:
                continue

            # Remove current position from lookup (we are moving)
            del cart_locations[(cart.x, cart.y)]

            # Calculate Next Position
            next_x, next_y = cart.x, cart.y
            if cart.direction == '^': next_y -= 1
            elif cart.direction == 'v': next_y += 1
            elif cart.direction == '<': next_x -= 1
            elif cart.direction == '>': next_x += 1

            # Check for Collision
            if (next_x, next_y) in cart_locations:
                # CRASH!
                other_cart = cart_locations[(next_x, next_y)]
                
                # Mark both as crashed
                cart.crashed = True
                other_cart.crashed = True
                
                # Remove the other cart from lookup immediately so no one else hits it
                del cart_locations[(next_x, next_y)]
                # (We don't add ourselves to lookup either)
                continue

            # Move Cart
            cart.x = next_x
            cart.y = next_y
            
            # Update lookup with new position
            cart_locations[(cart.x, cart.y)] = cart

            # Handle Track Logic
            # (Bounds check to be safe, though padding should prevent this)
            if next_y < 0 or next_y >= len(grid) or next_x < 0 or next_x >= len(grid[0]):
                print(f"Error: Cart went off map at {next_x},{next_y}")
                cart.crashed = True
                continue

            track = grid[next_y][next_x]

            if track == '+':
                # Intersection: Left -> Straight -> Right
                turn = cart.intersection_count % 3
                cart.intersection_count += 1
                
                if turn == 0: # Left
                    if cart.direction == '^': cart.direction = '<'
                    elif cart.direction == '<': cart.direction = 'v'
                    elif cart.direction == 'v': cart.direction = '>'
                    elif cart.direction == '>': cart.direction = '^'
                elif turn == 2: # Right
                    if cart.direction == '^': cart.direction = '>'
                    elif cart.direction == '>': cart.direction = 'v'
                    elif cart.direction == 'v': cart.direction = '<'
                    elif cart.direction == '<': cart.direction = '^'
            
            elif track == '/':
                if cart.direction == '^': cart.direction = '>'
                elif cart.direction == 'v': cart.direction = '<'
                elif cart.direction == '<': cart.direction = 'v'
                elif cart.direction == '>': cart.direction = '^'
                
            elif track == '\\':
                if cart.direction == '^': cart.direction = '<'
                elif cart.direction == 'v': cart.direction = '>'
                elif cart.direction == '<': cart.direction = '^'
                elif cart.direction == '>': cart.direction = 'v'

            # '|', '-', and ' ' do not change direction

        # End of Tick: Remove crashed carts
        carts = [c for c in carts if not c.crashed]

    if not carts:
        print("All carts crashed!")
    else:
        last = carts[0]
        print(f"Final Cart Position: {last.x},{last.y}")

if __name__ == "__main__":
    solve()