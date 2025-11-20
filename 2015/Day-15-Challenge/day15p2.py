import os
import re

# Total number of teaspoons available for the recipe
TOTAL_TEASPOONS = 100
# Target calorie count for Part Two
TARGET_CALORIES = 500

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

def calculate_score(amounts, ingredients, check_calories=False):
    """
    Calculates the final cookie score for a given set of ingredient amounts.
    If check_calories is True, returns 0 if total calories != TARGET_CALORIES.
    """
    
    # --- Check Calorie Constraint (NEW FOR PART 2) ---
    current_calories = 0
    if check_calories:
        for i, amount in enumerate(amounts):
            current_calories += amount * ingredients[i]['cal']
        
        if current_calories != TARGET_CALORIES:
            return 0 # Fail: Calorie constraint not met

    # --- Property Score Calculation ---
    properties = ['cap', 'dur', 'fla', 'tex']
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


def find_best_score_p2(ingredients):
    """
    Finds the highest-scoring cookie recipe that meets the calorie constraint 
    using recursive depth-first search (DFS).
    """
    N = len(ingredients)
    max_score = 0

    # The current DFS must also track the accumulated calorie count for early stopping 
    # if a partial mix already exceeds 500 calories (though not strictly necessary 
    # for correctness, it can be a useful optimization). 
    
    # Since we are checking the calorie constraint only at the final step, 
    # we just need to ensure the final calculation includes the check.
    
    def dfs(current_amounts, remaining_teaspoons, ingredient_index):
        nonlocal max_score
        
        if ingredient_index == N - 1:
            # Base Case: Last ingredient. Assign all remaining teaspoons to it.
            final_amounts = current_amounts + [remaining_teaspoons]
            
            # Check the score, enforcing the calorie constraint inside calculate_score
            score = calculate_score(final_amounts, ingredients, check_calories=True)
            max_score = max(max_score, score)
            return

        # Recursive Case: Distribute teaspoons to the current ingredient (0 to remaining)
        for amount in range(remaining_teaspoons + 1):
            dfs(current_amounts + [amount], 
                remaining_teaspoons - amount, 
                ingredient_index + 1)
            
    # Start DFS: 0 teaspoons used, 100 remaining, starting at ingredient 0
    dfs([], TOTAL_TEASPOONS, 0)
    
    return max_score


def solve_cookie_recipe(filepath):
    """
    Main function to orchestrate parsing and optimization for Part Two.
    """
    ingredients = parse_ingredients(filepath)
    if not ingredients:
        print("No ingredient data parsed.")
        return 0

    print(f"Total ingredients: {len(ingredients)}")
    print(f"Searching for optimal mix summing to {TOTAL_TEASPOONS} teaspoons ")
    print(f"WITH A CALORIE TOTAL OF EXACTLY {TARGET_CALORIES}...")
    
    final_score = find_best_score_p2(ingredients)
    
    return final_score

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting cookie recipe optimization (Part Two) using data from: {os.path.abspath(input_file)}\n")
    
    final_score = solve_cookie_recipe(input_file)
    
    print("\n" + "="*50)
    print("PART TWO: TOTAL SCORE OF THE HIGHEST-SCORING COOKIE (500 Calories):")
    print(f"SCORE: {final_score}")
    print("="*50)