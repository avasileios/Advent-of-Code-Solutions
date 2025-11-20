import os

# The total amount of eggnog to store
TARGET_LITERS = 150

def parse_containers(filepath):
    """
    Reads container capacities from the file, one per line.
    
    Returns:
        list: A list of integer container capacities.
    """
    containers = []
    
    try:
        # Robust path reading
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Container file not found at '{filepath}'")
        return []
    
    for line in lines:
        try:
            containers.append(int(line))
        except ValueError:
            print(f"Warning: Skipping non-integer line: {line}")
            continue
            
    return containers

def solve_container_combinations(filepath):
    """
    Uses recursive DFS to find the total number of combinations of containers 
    that sum exactly to TARGET_LITERS.
    """
    containers = parse_containers(filepath)
    if not containers:
        print("No container data loaded.")
        return 0

    # Optimization: Sorting the containers allows for early termination 
    # of branches if the current sum already exceeds the target.
    # containers.sort(reverse=True)
    
    N = len(containers)
    total_combinations = 0

    def find_combinations(index, current_sum):
        nonlocal total_combinations
        
        # Base Case 1: Target reached
        if current_sum == TARGET_LITERS:
            total_combinations += 1
            return
            
        # Base Case 2: Target exceeded or end of list reached
        if current_sum > TARGET_LITERS or index == N:
            return

        # Recursive Step: Iterate through the remaining containers starting from 'index'
        for i in range(index, N):
            
            # Action: Include the container at index i
            # We move to the next index (i + 1) to ensure we don't reuse the same physical container
            find_combinations(i + 1, current_sum + containers[i])

    # Start the DFS from index 0 with a sum of 0
    find_combinations(0, 0)
    
    return total_combinations

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting eggnog combination analysis for {TARGET_LITERS} liters using data from: {os.path.abspath(input_file)}\n")
    
    final_score = solve_container_combinations(input_file)
    
    print("\n" + "="*50)
    print(f"TOTAL NUMBER OF COMBINATIONS THAT FIT EXACTLY {TARGET_LITERS} LITERS:")
    print(f"SCORE: {final_score}")
    print("="*50)