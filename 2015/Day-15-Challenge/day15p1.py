import os
import re
from itertools import product # Used for a simplified distribution check

# Total number of teaspoons available for the recipe
TOTAL_TEASPOONS = 100

def parse_ingredients(filepath):
    """
    Reads ingredient properties from the file.
    
    Returns:
        list: List of dictionaries, one for each ingredient's properties.
    """
    ingredients = []
    
    try:
        # Robust path reading
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Instructions file not found at '{filepath}'")
        return []
    
    # Regex to capture all property values (capacity, durability, flavor, texture, calories)
    pattern = re.compile(
        r'(\w+):\s+capacity\s+(-?\d+),\s+durability\s+(-?\d+),\s+flavor\s+(-?\d+),\s+texture\s+(-?\d+),\s+calories\s+(-?\d+)'
    )
    
    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
            
        # Group 1 is the name, Groups 2-6 are the properties
        name = match.group(1)
        capacity, durability, flavor, texture, calories = map(int, match.groups()[1:])
        
        ingredients.append({
            'name': name,
            'cap': capacity,
            'dur': durability,
            'fla': flavor,
            'tex': texture,
            'cal': calories
        })
        
    return ingredients

def calculate_score(amounts, ingredients):
    """
    Calculates the final cookie score for a given set of ingredient amounts.
    """
    # The four scoring properties (calories is ignored in the final product)
    properties = ['cap', 'dur', 'fla', 'tex']
    
    # Calculate the total value for each property
    property_totals = []
    
    for prop in properties:
        total = 0
        for i, amount in enumerate(amounts):
            total += amount * ingredients[i][prop]
        
        # Apply the rule: negative totals become 0
        property_totals.append(max(0, total))
        
    # The final score is the product of the property totals
    final_score = 1
    for total in property_totals:
        final_score *= total
        
    return final_score


def find_best_score(ingredients):
    """
    Finds the highest-scoring cookie recipe using recursive depth-first search 
    (DFS) to explore all possible combinations that sum to TOTAL_TEASPOONS.
    """
    N = len(ingredients)
    max_score = 0

    # We use a helper function to perform the DFS
    # current_amounts: list of teaspoons used for ingredients processed so far
    # remaining_teaspoons: total left to distribute
    # ingredient_index: index of the ingredient currently being assigned
    def dfs(current_amounts, remaining_teaspoons, ingredient_index):
        nonlocal max_score
        
        if ingredient_index == N - 1:
            # Base Case: Last ingredient. Assign all remaining teaspoons to it.
            final_amounts = current_amounts + [remaining_teaspoons]
            
            # Since the amount is assigned to the last ingredient, the total 
            # is guaranteed to be 100. Check the score.
            score = calculate_score(final_amounts, ingredients)
            max_score = max(max_score, score)
            return

        # Recursive Case: Distribute teaspoons to the current ingredient (0 to remaining)
        # We must leave at least 0 teaspoons for the remaining N - 1 - ingredient_index ingredients.
        
        # Upper bound for the current amount: 
        # (Remaining teaspoons) - (minimum 0 for each of the remaining ingredients)
        # This is simply 0 to remaining_teaspoons
        
        for amount in range(remaining_teaspoons + 1):
            
            # Optimization: We could potentially cap the amount to save time, 
            # but for small N, exploring all branches is safe.
            
            dfs(current_amounts + [amount], 
                remaining_teaspoons - amount, 
                ingredient_index + 1)
            
    # Start DFS: 0 teaspoons used, 100 remaining, starting at ingredient 0
    dfs([], TOTAL_TEASPOONS, 0)
    
    return max_score


def solve_cookie_recipe(filepath):
    """
    Main function to orchestrate parsing and optimization.
    """
    ingredients = parse_ingredients(filepath)
    if not ingredients:
        print("No ingredient data parsed.")
        return 0

    print(f"Total ingredients: {len(ingredients)}")
    print(f"Searching for optimal mix summing to {TOTAL_TEASPOONS} teaspoons...")
    
    final_score = find_best_score(ingredients)
    
    return final_score

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting cookie recipe optimization using data from: {os.path.abspath(input_file)}\n")
    
    final_score = solve_cookie_recipe(input_file)
    
    print("\n" + "="*50)
    print("TOTAL SCORE OF THE HIGHEST-SCORING COOKIE:")
    print(f"SCORE: {final_score}")
    print("="*50)