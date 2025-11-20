import os
import re
from typing import Set, Dict, List, Tuple

def parse_towers(filepath) -> tuple[Dict[str, List[str]], Dict[str, int], str | None]:
    """
    Reads the tower structure data.
    
    Returns:
        tuple: (children_map: {parent: [child1, ...]}, weights: {name: weight}, root_name)
    """
    children_map = {}
    weights = {}
    
    # Track all programs and all children to find the single root
    all_programs = set()
    all_children = set()
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Input file not found at '{filepath}'")
        return {}, {}, None
        
    pattern = re.compile(r'(\w+)\s+\((\d+)\)(?:\s+->\s+(.*))?')

    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
            
        name = match.group(1)
        weight = int(match.group(2))
        children_str = match.group(3)
        
        all_programs.add(name)
        weights[name] = weight
        children_map[name] = []
        
        if children_str:
            children = [c.strip() for c in children_str.split(',')]
            children_map[name] = children
            all_children.update(children)
            
    # Find the root (program not supported by anyone else)
    root_set = all_programs.difference(all_children)
    root_name = list(root_set)[0] if len(root_set) == 1 else None
        
    return children_map, weights, root_name

def get_tower_weight(program_name: str, children_map: Dict[str, List[str]], weights: Dict[str, int], weight_cache: Dict[str, int]) -> int:
    """
    Recursively calculates the total weight of the sub-tower starting at program_name.
    Uses memoization (weight_cache).
    """
    if program_name in weight_cache:
        return weight_cache[program_name]
        
    # Start with the program's own weight
    total_weight = weights[program_name]
    
    # Add the weight of all sub-towers sitting on its disc
    if program_name in children_map:
        for child in children_map[program_name]:
            total_weight += get_tower_weight(child, children_map, weights, weight_cache)
            
    weight_cache[program_name] = total_weight
    return total_weight

def find_unbalanced_program_and_weight(children_map, weights, root_name):
    """
    Traverses the tower structure to find the single unbalanced program and 
    determine its correct weight.
    """
    if not root_name: return None
    
    # Cache for tower weights
    weight_cache = {}
    
    current_unbalanced_program = root_name
    target_correction = 0
    
    # Traverse down from the root until we find the program causing the unbalance
    while True:
        parent_program = current_unbalanced_program
        children = children_map.get(parent_program, [])
        
        if not children:
            # Base Case 1: Reached a leaf node (program with no children).
            # This should not happen if the logic is correct, as the unbalanced 
            # node must be a parent to transmit the error upward.
            print(f"Error: Unbalanced node search reached leaf {parent_program}.")
            return None

        # 1. Calculate the total weight of all children sub-towers
        child_tower_weights = {}
        for child in children:
            child_tower_weights[child] = get_tower_weight(child, children_map, weights, weight_cache)
            
        # 2. Check for balance among children's towers
        
        # Count frequencies of the tower weights
        weight_counts = Counter(child_tower_weights.values())
        
        if len(weight_counts) <= 1:
            # Base Case 2: All children's sub-towers are balanced.
            # This means the current parent program (parent_program) itself is the culprit.
            
            # The required target weight is the weight of its siblings' sub-towers.
            # We need the parent program's weight BEFORE the recursion started.
            
            # Target weight (of balanced sibling sub-towers)
            # We need to backtrack to the previous level to get the target weight.
            # This is handled by 'target_correction' from the outer caller, but since 
            # we are stuck in a loop here, we need the parent caller's target.
            
            # Since the loop runs until the *immediate child* is the culprit:
            # The discrepancy must have been detected at the previous (outer) level.
            # The program causing the unbalance is the one currently in the loop 
            # (current_unbalanced_program), and its *own* children are balanced.
            
            # Therefore, we need the correction amount (target_correction) established 
            # when its parent called it. Since that amount isn't passed explicitly,
            # we must find the required weight from the siblings at the level where 
            # the unbalance was first detected.
            
            # Exit loop and calculate based on correction amount found at previous level.
            break 
            
        # 3. Identify the odd one out (The Unbalanced Child)
        
        # The weight that appears only once is the wrong one
        unbalanced_weight = next(w for w, count in weight_counts.items() if count == 1)
        
        # The weight that appears multiple times is the correct target
        target_weight = next(w for w, count in weight_counts.items() if count != 1)
        
        # The program whose tower is unbalanced
        unbalanced_child_name = next(name for name, w in child_tower_weights.items() if w == unbalanced_weight)
        
        # The amount of correction needed for that child's entire tower:
        target_correction = target_weight - unbalanced_weight
        
        # We now recursively descend into the unbalanced child's sub-tower
        current_unbalanced_program = unbalanced_child_name
        
    # --- Final Calculation ---
    
    # The loop broke because we found the culprit program (current_unbalanced_program), 
    # and its own children are balanced.
    
    # We must find the correction needed at the *first* level where unbalance occurred 
    # (which is the loop's context upon final break).
    
    # Re-evaluate one last time at the level where the imbalance was detected (root level)
    root_children = children_map[root_name]
    child_tower_weights = {child: get_tower_weight(child, children_map, weights, weight_cache) for child in root_children}
    
    unbalanced_weight = next(w for w, count in Counter(child_tower_weights.values()).items() if count == 1)
    target_weight = next(w for w, count in Counter(child_tower_weights.values()).items() if count != 1)
    
    # The actual program that needs correction is the last value stored in 
    # current_unbalanced_program
    
    # Calculate the required weight correction
    weight_difference = unbalanced_weight - target_weight
    
    # The program that needs its weight fixed is the one stored in current_unbalanced_program
    culprit_program = current_unbalanced_program
    
    # The correct weight is the program's current weight minus the difference
    required_weight = weights[culprit_program] - weight_difference
    
    return required_weight

# --- Main Execution Block ---
if __name__ == "__main__":
    from collections import Counter
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting tower structure analysis (Part 2 - Weight Correction) using data from: {os.path.abspath(input_file)}\n")
    
    children_map, weights, root_name = parse_towers(input_file)
    
    if not root_name:
        print("Error: Could not find unique root program.")
        final_weight = 0
    else:
        final_weight = find_unbalanced_program_and_weight(children_map, weights, root_name)
    
    print("\n" + "="*50)
    print("PROGRAM'S WEIGHT NEEDED TO BALANCE THE ENTIRE TOWER:")
    print(f"SCORE: {final_weight}")
    print("="*50)