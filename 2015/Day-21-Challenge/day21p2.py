import os
from itertools import combinations

# --- Constants ---
PLAYER_HP_START = 100
# Placeholder constants used if file reading fails
BOSS_HP_START = 100 
BOSS_DAMAGE = 8     
BOSS_ARMOR = 2      

# --- Shop Data ---
SHOP = {
    'Weapons': [
        (8, 4, 0),   # (Cost, Damage, Armor)
        (10, 5, 0),
        (25, 6, 0),
        (40, 7, 0),
        (74, 8, 0),
    ],
    'Armor': [
        (0, 0, 0),   # Option for buying NO armor (Cost 0, Stats 0)
        (13, 0, 1),
        (31, 0, 2),
        (53, 0, 3),
        (75, 0, 4),
        (102, 0, 5),
    ],
    'Rings': [
        (0, 0, 0),   # Slot for buying NO Ring 1
        (0, 0, 0),   # Slot for buying NO Ring 2
        (25, 1, 0),  # Damage +1
        (50, 2, 0),  # Damage +2
        (100, 3, 0), # Damage +3
        (20, 0, 1),  # Defense +1
        (40, 0, 2),  # Defense +2
        (80, 0, 3),  # Defense +3
    ]
}

def parse_boss_stats(filepath):
    """
    Reads the boss's stats from the input file.
    """
    stats = {}
    # Use robust path construction
    absolute_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
    
    try:
        with open(absolute_filepath, 'r') as f:
            for line in f:
                if 'Hit Points' in line:
                    stats['HP'] = int(line.split(':')[1].strip())
                elif 'Damage' in line:
                    stats['Damage'] = int(line.split(':')[1].strip())
                elif 'Armor' in line:
                    stats['Armor'] = int(line.split(':')[1].strip())
    except FileNotFoundError:
        print(f"Error: Boss stats file not found at '{absolute_filepath}'. Using placeholders.")
        return {'HP': BOSS_HP_START, 'Damage': BOSS_DAMAGE, 'Armor': BOSS_ARMOR}
    
    if len(stats) < 3:
        print("Warning: Incomplete boss stats in file. Using placeholders.")
        return {'HP': BOSS_HP_START, 'Damage': BOSS_DAMAGE, 'Armor': BOSS_ARMOR}
        
    return stats


def player_wins(player_damage, player_armor, boss_hp, boss_damage, boss_armor):
    """
    Simulates the combat round by round. Returns True if the player wins.
    """
    player_hp = PLAYER_HP_START
    
    # Calculate effective damage (min 1)
    player_effective_damage = max(1, player_damage - boss_armor)
    boss_effective_damage = max(1, boss_damage - player_armor)
    
    # Combat Loop (Player always goes first)
    while True:
        # Player's Turn
        boss_hp -= player_effective_damage
        if boss_hp <= 0:
            return True
        
        # Boss's Turn
        player_hp -= boss_effective_damage
        if player_hp <= 0:
            return False

def solve_rpg_puzzle(filepath):
    """
    Brute-forces all valid item combinations to find the minimum cost to win (P1)
    and the maximum cost to lose (P2).
    """
    boss_stats = parse_boss_stats(filepath)
    BOSS_HP = boss_stats['HP']
    BOSS_DAMAGE = boss_stats['Damage']
    BOSS_ARMOR = boss_stats['Armor']
    
    min_winning_cost = float('inf')
    max_losing_cost = 0 # Initialize to 0 for maximization

    # Extract item lists
    weapons = SHOP['Weapons']
    armors = SHOP['Armor']
    all_rings = SHOP['Rings'] # Includes 2 dummy slots (0, 1) + 6 unique purchasable rings (2-7)

    # --- Brute Force All Valid Combinations ---
    
    # Rings selection: Total 8 unique items available for rings (indices 0 to 7)
    # We choose combinations of 2 distinct indices. This covers:
    # 0 Rings (indices 0, 1)
    # 1 Ring (index 0 or 1, and index 2-7)
    # 2 Rings (index 2-7, and index 3-7)
    
    ring_indices = list(range(len(all_rings)))
    
    # Generate all unique combinations of two distinct indices (slots).
    # Since combinations(iterable, 2) only produces unique pairs, we need to 
    # add the special case for the two dummy slots (0 rings).
    ring_combos_indices = list(combinations(ring_indices, 2))
    ring_combos_indices.append((0, 1)) # Add the 0-ring case (No Ring 1, No Ring 2)

    
    # 1. Choose exactly one Weapon
    for w_cost, w_dmg, w_arm in weapons:
        
        # 2. Choose zero or one Armor
        for a_cost, a_dmg, a_arm in armors:
            
            # 3. Choose 0, 1, or 2 Rings
            for r_index1, r_index2 in ring_combos_indices:
                r1_cost, r1_dmg, r1_arm = all_rings[r_index1]
                r2_cost, r2_dmg, r2_arm = all_rings[r_index2]
                
                # Check for item overlap: If both rings are actual purchasable rings, 
                # they must not be the same item (same index). This is implicitly handled
                # by combinations() but a logical check for the dummy slots is needed.
                if r_index1 > 1 and r_index2 > 1 and r_index1 == r_index2:
                    # Safety check for two rings from the purchasable set (not needed with combinations)
                    continue 

                # --- Calculate Total Stats and Cost ---
                
                total_cost = w_cost + a_cost + r1_cost + r2_cost
                player_damage = w_dmg + a_dmg + r1_dmg + r2_dmg
                player_armor = w_arm + a_arm + r1_arm + r2_arm
                
                # --- Simulate the Fight ---
                player_won = player_wins(player_damage, player_armor, BOSS_HP, BOSS_DAMAGE, BOSS_ARMOR)
                
                if player_won:
                    # Part 1 Logic: Find the least amount to WIN
                    min_winning_cost = min(min_winning_cost, total_cost)
                else:
                    # Part 2 Logic: Find the MAX amount to LOSE
                    max_losing_cost = max(max_losing_cost, total_cost)
                    
    return min_winning_cost, max_losing_cost

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting RPG Battle Solver (Min Win, Max Lose) using data from: {os.path.abspath(input_file)}\n")
    
    min_win_cost, max_lose_cost = solve_rpg_puzzle(input_file)
    
    print("\n" + "="*50)
    print("PART 1: LEAST AMOUNT OF GOLD TO SPEND AND WIN:")
    print(f"SCORE: {min_win_cost}")
    print("-" * 50)
    print("PART 2: MOST AMOUNT OF GOLD TO SPEND AND STILL LOSE:")
    print(f"SCORE: {max_lose_cost}")
    print("="*50)