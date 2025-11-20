import os

def calculate_required_paper(l: int, w: int, h: int) -> int:
    """
    Calculates the total square feet of wrapping paper required for one box.
    Required Paper = Surface Area + Area of the Smallest Side.
    """
    # Calculate the area of the three unique sides
    side1 = l * w
    side2 = w * h
    side3 = h * l
    
    # Calculate Surface Area (2 * side1 + 2 * side2 + 2 * side3)
    surface_area = 2 * (side1 + side2 + side3)
    
    # Calculate the area of the smallest side (slack)
    smallest_side_area = min(side1, side2, side3)
    
    # Total required paper
    total_paper = surface_area + smallest_side_area
    
    return total_paper

def solve_wrapping_puzzle(dimensions_file):
    """
    Reads all present dimensions and sums the total required wrapping paper.
    """
    try:
        # Robust path reading
        with open(dimensions_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Dimensions file not found at '{dimensions_file}'")
        return 0
    
    total_paper_ordered = 0
    
    for line in lines:
        try:
            # Dimensions are expected to be in l x w x h format
            l, w, h = map(int, line.split('x'))
            
            paper = calculate_required_paper(l, w, h)
            total_paper_ordered += paper
            
        except ValueError:
            print(f"Warning: Skipping invalid line format: {line}")
            continue
            
    return total_paper_ordered

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction using the current script's directory and 'input.txt'
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting wrapping paper calculation using dimensions from: {os.path.abspath(input_file)}\n")
    
    final_total = solve_wrapping_puzzle(input_file)
    
    print("\n" + "="*50)
    print("TOTAL SQUARE FEET OF WRAPPING PAPER TO ORDER:")
    print(f"SCORE: {final_total}")
    print("="*50)