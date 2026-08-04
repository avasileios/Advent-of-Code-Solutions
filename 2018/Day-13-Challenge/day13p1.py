import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

class Cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.dir = direction
        self.turns = 0  # 0: left, 1: straight, 2: right
        self.crashed = False

    def move(self, track_map):
        # Update position based on direction
        if self.dir == '^': self.y -= 1
        elif self.dir == 'v': self.y += 1
        elif self.dir == '<': self.x -= 1
        elif self.dir == '>': self.x += 1

        # Interact with tracks
        track = track_map[self.y][self.x]
        
        if track == '+':
            self.turn_at_intersection()
        elif track in '/\\':
            self.turn_at_curve(track)

    def turn_at_intersection(self):
        # Directions ordered clockwise: ^ > v <
        dirs = ['^', '>', 'v', '<']
        idx = dirs.index(self.dir)
        
        if self.turns == 0: # Left
            self.dir = dirs[(idx - 1) % 4]
        elif self.turns == 2: # Right
            self.dir = dirs[(idx + 1) % 4]
        # (self.turns == 1 is straight, so do nothing)
        
        self.turns = (self.turns + 1) % 3

    def turn_at_curve(self, curve):
        if curve == '/':
            mapping = {'^': '>', 'v': '<', '<': 'v', '>': '^'}
        else: # curve == '\'
            mapping = {'^': '<', 'v': '>', '<': '^', '>': 'v'}
        self.dir = mapping[self.dir]

def solve():
    with open(file_path, 'r') as f:
        lines = [list(line.replace('\n', '')) for line in f.readlines()]

    carts = []
    track_map = []
    
    # Extract carts and clean map
    for y, row in enumerate(lines):
        track_row = []
        for x, char in enumerate(row):
            if char in '^v<>':
                carts.append(Cart(x, y, char))
                track_row.append('|' if char in '^v' else '-')
            else:
                track_row.append(char)
        track_map.append(track_row)

    while True:
        # Sort carts: top-to-bottom, left-to-right
        carts.sort(key=lambda c: (c.y, c.x))
        
        for cart in carts:
            cart.move(track_map)
            
            # Check for crash
            for other in carts:
                if cart != other and cart.x == other.x and cart.y == other.y:
                    return f"{cart.x},{cart.y}"

if __name__ == "__main__":
    print(f"First crash location: {solve()}")