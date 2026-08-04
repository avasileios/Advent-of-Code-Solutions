def get_power_level(x, y, serial):
    rack_id = x + 10
    power = (rack_id * y + serial) * rack_id
    # Extract the hundreds digit
    hundreds = (power // 100) % 10
    return hundreds - 5

def solve_fuel_grid(serial):
    # Initialize 300x300 grid (using 1-based indexing for convenience)
    grid = [[0] * 301 for _ in range(301)]
    
    for y in range(1, 301):
        for x in range(1, 301):
            grid[y][x] = get_power_level(x, y, serial)
            
    max_power = -float('inf')
    best_coords = (0, 0)
    
    # Check every possible 3x3 square
    # Range is 1 to 298 because a 3x3 square at 298 covers 298, 299, 300
    for y in range(1, 299):
        for x in range(1, 299):
            current_sum = 0
            # Sum the 3x3 area
            for dy in range(3):
                for dx in range(3):
                    current_sum += grid[y + dy][x + dx]
            
            if current_sum > max_power:
                max_power = current_sum
                best_coords = (x, y)
                
    return best_coords

if __name__ == "__main__":
    serial_number = 9995
    x, y = solve_fuel_grid(serial_number)
    print(f"The top-left coordinate of the best 3x3 square is: {x},{y}")