def solve_variable_fuel_grid(serial):
    size = 300
    # Initialize grid with 0s (301x301 for 1-based indexing)
    sat = [[0] * (size + 1) for _ in range(size + 1)]
    
    # Step 1: Build the Summed-Area Table
    for y in range(1, size + 1):
        for x in range(1, size + 1):
            # Calculate power level for this specific cell
            rack_id = x + 10
            power = (rack_id * y + serial) * rack_id
            hundreds = (power // 100) % 10
            cell_power = hundreds - 5
            
            # Build SAT: current + top + left - diagonal_top_left
            sat[y][x] = cell_power + sat[y-1][x] + sat[y][x-1] - sat[y-1][x-1]
            
    max_power = -float('inf')
    best_identifier = ""
    
    # Step 2: Check every square size from 1 to 300
    for s in range(1, size + 1):
        for y in range(s, size + 1):
            for x in range(s, size + 1):
                # Calculate sum using the 4-point SAT formula
                # Square ends at (x, y), top-left is (x-s+1, y-s+1)
                total = sat[y][x] - sat[y-s][x] - sat[y][x-s] + sat[y-s][x-s]
                
                if total > max_power:
                    max_power = total
                    best_identifier = f"{x-s+1},{y-s+1},{s}"
                    
    return best_identifier

if __name__ == "__main__":
    serial_number = 9995
    print(f"Calculating... (this may take 5-10 seconds)")
    result = solve_variable_fuel_grid(serial_number)
    print(f"The X,Y,size identifier is: {result}")