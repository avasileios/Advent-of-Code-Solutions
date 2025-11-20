import os
import math

# Your puzzle input
TARGET_SQUARE = 312051

def find_spiral_distance(N: int) -> int:
    """
    Finds the Manhattan distance of square N from the center (square 1).
    """
    if N == 1:
        return 0

    # 1. Determine the Ring (R)
    # The side length S of the square containing N is the smallest odd integer 
    # greater than or equal to sqrt(N).
    
    # Calculate the square root
    sqrt_n = math.sqrt(N)
    
    # Find the smallest odd integer S >= sqrt_n
    S = math.ceil(sqrt_n)
    if S % 2 == 0:
        S += 1
        
    # Ring number R (distance from center to the middle of the side)
    R = (S - 1) // 2
    
    # Value of the largest corner in this ring
    C_max = S * S 
    
    # 2. Find the position on the sides
    side_length = S - 1 # Length of one side of the ring (e.g., S=5, length=4)
    half_side = side_length // 2 # Distance from corner to middle of the side
    
    # The sides are traced counter-clockwise starting from the bottom-right corner (C_max).
    # Side 1: Bottom row (Right -> Left)
    # Side 2: Left column (Bottom -> Top)
    # Side 3: Top row (Left -> Right)
    # Side 4: Right column (Top -> Bottom, ending at C_max)
    
    # We trace back from C_max
    distance_from_max = C_max - N 
    
    # Since the path is traced counter-clockwise, the sides are: Right, Top, Left, Bottom
    
    # Side 1 (Right column, Bottom -> Top)
    # Start: (R, -R). End: (R, R). Length: 2R.
    if distance_from_max < side_length:
        # N is on the Right side.
        # Position offset from corner = distance_from_max.
        # Coordinate Y = -R + distance_from_max.
        y_coord = -R + distance_from_max
        x_coord = R
        
    # Side 2 (Top row, Right -> Left)
    elif distance_from_max < 2 * side_length:
        # N is on the Top side.
        # Distance into side: distance_from_max - side_length
        dist_into_side = distance_from_max - side_length
        # Coordinate X = R - dist_into_side.
        x_coord = R - dist_into_side
        y_coord = R
        
    # Side 3 (Left column, Top -> Bottom)
    elif distance_from_max < 3 * side_length:
        # N is on the Left side.
        dist_into_side = distance_from_max - 2 * side_length
        # Coordinate Y = R - dist_into_side.
        y_coord = R - dist_into_side
        x_coord = -R
        
    # Side 4 (Bottom row, Left -> Right)
    else:
        # N is on the Bottom side.
        dist_into_side = distance_from_max - 3 * side_length
        # Coordinate X = -R + dist_into_side.
        x_coord = -R + dist_into_side
        y_coord = -R

    # 3. Calculate Manhattan Distance: |x| + |y|
    # Note: The distance from (x, y) to (0, 0) is |x| + |y|.
    # The distance from the center of the side (x_c, y_c) to the center (0, 0) is R.
    # The required distance is R + |x - x_c| or R + |y - y_c|.
    
    # The actual calculation for Manhattan distance relies on the distance from the 
    # identified coordinate (x_coord, y_coord) to the origin (0, 0).
    
    return abs(x_coord) + abs(y_coord)

# --- Main Execution Block ---
if __name__ == "__main__":
    
    final_steps = find_spiral_distance(TARGET_SQUARE)
    
    print("\n" + "="*50)
    print(f"STEPS REQUIRED TO CARRY DATA FROM SQUARE {TARGET_SQUARE} TO ACCESS PORT (1):")
    print(f"SCORE: {final_steps}")
    print("="*50)