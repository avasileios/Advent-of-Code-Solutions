import os
from itertools import combinations

# --- Constants ---
PLAYER_HP_START = 100
BOSS_HP_START = 100 # Placeholder - Will be updated by input
BOSS_DAMAGE = 8     # Placeholder - Will be updated by input
BOSS_ARMOR = 2      # Placeholder - Will be updated by input

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
        (0, 0, 0),   # Option for buying NO first ring
        (0, 0, 0),   # Option for buying NO second ring (Total 0-2 rings)
        (25, 1, 0),
        (50, 2, 0),
        (100, 3, 0),
        (20, 0, 1),
        (40, 0, 2),
        (80, 0, 3),
    ]
}
# The two "Cost 0" rings allow us to easily generate combinations of 0, 1, or 2 unique rings.

def parse_boss_stats(filepath):
    """
    Reads the boss's stats from the input file.
    """
    stats = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                if 'Hit Points' in line:
                    stats['HP'] = int(line.split(':')[1].strip())
                elif 'Damage' in line:
                    stats['Damage'] = int(line.split(':')[1].strip())
                elif 'Armor' in line:
                    stats['Armor'] = int(line.split(':')[1].strip())
    except FileNotFoundError:
        print(f"Error: Boss stats file not found at '{filepath}'. Using placeholders.")
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
    Brute-forces all valid item combinations to find the minimum gold cost 
    that results in the player winning.
    """
    boss_stats = parse_boss_stats(filepath)
    BOSS_HP = boss_stats['HP']
    BOSS_DAMAGE = boss_stats['Damage']
    BOSS_ARMOR = boss_stats['Armor']
    
    min_winning_cost = float('inf')
    
    # Extract item lists without the cost/stat structure yet
    weapons = SHOP['Weapons']
    armors = SHOP['Armor']
    
    # The Rings list includes 2 zero-cost placeholders for 0-2 rings total
    all_rings = SHOP['Rings']
    
    # --- Brute Force All Valid Combinations ---
    
    # 1. Choose exactly one Weapon
    for w_cost, w_dmg, w_arm in weapons:
        
        # 2. Choose zero or one Armor (iterate through all armor options, including the cost=0 dummy)
        for a_cost, a_dmg, a_arm in armors:
            
            # 3. Choose 0, 1, or 2 Rings (non-overlapping)
            # The 'all_rings' list includes two cost=0 dummies (indices 0 and 1).
            # Indices 2 through 7 are the unique purchasable rings.
            
            # We generate all combinations of 0, 1, or 2 rings from the purchasable set 
            # (indices 2 through 7) plus the two dummy slots (indices 0 and 1).
            
            # We use combinations of size 2 from the ENTIRE list of rings (9 total items).
            # This covers: (dummy1, dummy2), (dummy1, RingX), (RingX, RingY).
            # Total unique items in list: 9. We pick 2.
            
            # NOTE: We must ensure we never select the same purchasable ring twice, 
            # and that we select exactly 2 slots in the final build (which can be the dummy slots).
            
            purchasable_rings = all_rings[2:] # Actual rings
            
            # Generate combinations of 0, 1, or 2 actual rings, padding with dummies
            
            # Combination size 0 (All dummies: 1 way)
            ring_set = [ (0, 0, 0), (0, 0, 0) ]
            
            # 0 Rings (Dummy + Dummy)
            r_combos = [ ((0, 0, 0), (0, 0, 0)) ] 
            
            # 1 Ring (Dummy + RingX)
            for r_item in purchasable_rings:
                r_combos.append( (r_item, (0, 0, 0)) ) 
            
            # 2 Unique Rings (RingX + RingY)
            for r_item1, r_item2 in combinations(purchasable_rings, 2):
                 r_combos.append( (r_item1, r_item2) ) 
                 
            # Note: We must ensure we don't count the 1-ring case twice due to item order.
            # The combination approach handles this neatly: pick 2 distinct slots from the 9 total options.
            
            # Let's simplify and use the full list of purchasable items (8 items) and pick 2:
            all_ring_options = [ (0, 0, 0) ] + purchasable_rings
            
            # Combinations of 2 items from the list of (No Ring) + (All Rings) 
            # This covers 0 rings (No Ring, No Ring), 1 ring (No Ring, RingX), 2 rings (RingX, RingY)
            
            # Use combinations of size 2 from the index list 0..8 (9 options total)
            ring_options_indices = list(range(len(all_rings)))
            
            # Get all unique combinations of two distinct indices
            # Note: Index 0 and 1 are the two "No Ring" slots.
            
            # Correct approach: Group all 8 items (1 dummy, 6 actual, 1 dummy)
            # No, the shop list is: 2 cost-zero dummies, 6 actual rings. Total 8 options.
            
            # The most robust way is to select 2 distinct slots from the full set of 9 items:
            # 2 dummy slots (0, 1) + 6 unique rings (2-7).
            
            ring_indices = list(range(len(all_rings))) # [0, 1, ..., 7] (9 total items)
            
            # Generate all combinations of two distinct indices
            ring_combos_indices = list(combinations(ring_indices, 2))
            
            # Add the case where 0 rings are bought (the two dummy slots 0 and 1)
            ring_combos_indices.append((0, 1))

            
            for r_index1, r_index2 in ring_combos_indices:
                r1_cost, r1_dmg, r1_arm = all_rings[r_index1]
                r2_cost, r2_dmg, r2_arm = all_rings[r_index2]
                
                # Check for overlap: If both rings are actual purchasable rings, 
                # they must not be the same item (same index).
                if r_index1 > 1 and r_index1 == r_index2:
                    continue # Should not happen with combinations(), but a safeguard.

                # Sum up all costs and stats for this full combination
                
                # Total Cost
                total_cost = w_cost + a_cost + r1_cost + r2_cost
                
                # Total Damage
                player_damage = w_dmg + a_dmg + r1_dmg + r2_dmg
                
                # Total Armor
                player_armor = w_arm + a_arm + r1_arm + r2_arm
                
                # Simulate the fight
                if player_wins(player_damage, player_armor, BOSS_HP, BOSS_DAMAGE, BOSS_ARMOR):
                    min_winning_cost = min(min_winning_cost, total_cost)
                    
    return min_winning_cost

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    # Need to run a small custom parse for the input file's format
    # The input file is expected to contain the boss stats: HP, Damage, Armor
    
    print(f"Starting RPG Battle Solver (Min Cost) using data from: {os.path.abspath(input_file)}\n")
    
    final_score = solve_rpg_puzzle(input_file)
    
    print("\n" + "="*50)
    print("LEAST AMOUNT OF GOLD TO SPEND AND STILL WIN:")
    print(f"SCORE: {final_score}")
    print("="*50)