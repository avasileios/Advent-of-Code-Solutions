import os
import re
import heapq

# --- Battle Constants ---
PLAYER_HP_START = 50
PLAYER_MANA_START = 500
TARGET_MANA = float('inf')

# Spells definition: (Cost, Damage, Heal, Duration, Mana_Gain, Armor)
SPELLS = {
    'Missile':   (53, 4, 0, 0, 0, 0),
    'Drain':     (73, 2, 2, 0, 0, 0),
    'Shield':    (113, 0, 0, 6, 0, 7), # Armor applied on turn start, lasts 6 turns (6 applications)
    'Poison':    (173, 0, 0, 6, 0, 0), # Damage applied on turn start, lasts 6 turns (6 applications)
    'Recharge':  (229, 0, 0, 5, 101, 0), # Mana applied on turn start, lasts 5 turns (5 applications)
}

def parse_boss_stats(filepath):
    """
    Reads the boss's stats from the input file.
    """
    stats = {}
    absolute_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
    
    try:
        with open(absolute_filepath, 'r') as f:
            for line in f:
                if 'Hit Points' in line:
                    stats['HP'] = int(line.split(':')[1].strip())
                elif 'Damage' in line:
                    stats['Damage'] = int(line.split(':')[1].strip())
    except FileNotFoundError:
        print(f"Error: Boss stats file not found at '{absolute_filepath}'.")
        # Use common placeholder stats if file is missing/corrupted
        return {'HP': 71, 'Damage': 10} 
    
    if len(stats) < 2:
        print("Warning: Incomplete boss stats in file. Using placeholders.")
        return {'HP': 71, 'Damage': 10}
        
    return stats

def apply_effects(state, mana_spent, is_player_turn=True):
    """
    Applies effects and updates state at the start of the turn.
    
    Returns:
        (new_state, new_mana_spent, current_armor, current_poison_dmg)
    """
    
    # Unpack current state
    p_hp, p_mana, b_hp, s_timer, p_timer, r_timer = state
    
    current_armor = 0
    current_poison_dmg = 0
    
    # 1. Apply Effects (Decay)
    
    # Recharge
    if r_timer > 0:
        p_mana += 101
        r_timer -= 1
        
    # Poison
    if p_timer > 0:
        b_hp -= 3
        p_timer -= 1
        
    # Shield
    if s_timer > 0:
        current_armor = 7
        s_timer -= 1
        
    # 2. Check for Boss Death after effects (Poison can win the game)
    if b_hp <= 0:
        # Victory achieved. Update and return.
        return (p_hp, p_mana, b_hp, s_timer, p_timer, r_timer), mana_spent, 0, 0, True

    # 3. Return updated values
    new_state = (p_hp, p_mana, b_hp, s_timer, p_timer, r_timer)
    return new_state, mana_spent, current_armor, 0, False # current_poison_dmg is always 0 for next step damage


def solve_wizard_battle(filepath):
    """
    Finds the least amount of mana required to win the fight using Dijkstra's/BFS.
    """
    boss_stats = parse_boss_stats(filepath)
    BOSS_HP_START = boss_stats['HP']
    BOSS_DAMAGE = boss_stats['Damage']
    
    # The state is (p_hp, p_mana, b_hp, s_timer, p_timer, r_timer)
    initial_state = (PLAYER_HP_START, PLAYER_MANA_START, BOSS_HP_START, 0, 0, 0)
    
    # Priority Queue stores: (mana_spent, p_hp, p_mana, b_hp, s_timer, p_timer, r_timer)
    pq = [(0, PLAYER_HP_START, PLAYER_MANA_START, BOSS_HP_START, 0, 0, 0)]
    
    # Dictionary to track minimum mana spent to reach a given game state
    # Key: (p_hp, p_mana, b_hp, s_timer, p_timer, r_timer) -> Value: min_mana_spent
    min_mana_map = {initial_state: 0}
    
    min_winning_mana = float('inf')

    while pq:
        mana_spent, p_hp, p_mana, b_hp, s_timer, p_timer, r_timer = heapq.heappop(pq)
        current_state = (p_hp, p_mana, b_hp, s_timer, p_timer, r_timer)

        # Optimization: If we found a cheaper way to reach this state, skip
        if mana_spent > min_mana_map.get(current_state, float('inf')):
            continue

        # Check for immediate win (should only happen if state was popped after a victory, 
        # but we check for win only after the Boss turn)
        # We ensure we don't proceed with paths already over the current minimum win cost
        if mana_spent >= min_winning_mana:
            continue

        
        # ----------------------------------------------------
        # --- 1. PLAYER TURN: Apply Effects & Cast Spell ---
        # ----------------------------------------------------
        
        # Apply effects at the start of the Player's turn
        (p_hp_eff, p_mana_eff, b_hp_eff, s_timer_eff, p_timer_eff, r_timer_eff), _, current_armor_eff, _, victory = \
            apply_effects(current_state, mana_spent, is_player_turn=True)

        if victory:
            min_winning_mana = min(min_winning_mana, mana_spent)
            continue
        
        # Check if Player dies from Poison/etc. (Shouldn't happen on Player's turn start, but safe)
        if p_hp_eff <= 0:
            continue 

        # Try casting all 5 spells
        for spell_name, (cost, dmg, heal, duration, mana_gain, armor) in SPELLS.items():
            
            # Check affordability
            if p_mana_eff < cost:
                continue

            # Check if effect is already active
            if spell_name == 'Shield' and s_timer_eff > 0:
                continue
            if spell_name == 'Poison' and p_timer_eff > 0:
                continue
            if spell_name == 'Recharge' and r_timer_eff > 0:
                continue
                
            # --- Cast Spell ---
            
            new_mana_spent = mana_spent + cost
            p_mana_spell = p_mana_eff - cost
            
            p_hp_spell = p_hp_eff + heal
            b_hp_spell = b_hp_eff - dmg
            
            s_timer_spell, p_timer_spell, r_timer_spell = s_timer_eff, p_timer_eff, r_timer_eff
            
            # Set new effect timer if applicable
            if duration > 0:
                if spell_name == 'Shield':
                    s_timer_spell = duration
                elif spell_name == 'Poison':
                    p_timer_spell = duration
                elif spell_name == 'Recharge':
                    r_timer_spell = duration
            
            # Check for Boss Death after instant spell damage
            if b_hp_spell <= 0:
                min_winning_mana = min(min_winning_mana, new_mana_spent)
                continue
            
            # ----------------------------------------------------
            # --- 2. BOSS TURN: Apply Effects & Attack ---
            # ----------------------------------------------------
            
            state_after_spell = (p_hp_spell, p_mana_spell, b_hp_spell, 
                                 s_timer_spell, p_timer_spell, r_timer_spell)
            
            # 2a. Apply Effects at start of Boss's turn
            (p_hp_boss_eff, p_mana_boss_eff, b_hp_boss_eff, s_timer_boss_eff, p_timer_boss_eff, r_timer_boss_eff), _, current_armor_boss_eff, _, victory = \
                apply_effects(state_after_spell, new_mana_spent, is_player_turn=False)
                
            if victory:
                min_winning_mana = min(min_winning_mana, new_mana_spent)
                continue
            
            # 2b. Boss Attack
            # The armor value comes from the effect applied at the START of the turn.
            
            # Boss damage is calculated using current_armor_boss_eff (which is 7 if shield is active, 0 otherwise)
            boss_effective_damage = max(1, BOSS_DAMAGE - current_armor_boss_eff)
            p_hp_final = p_hp_boss_eff - boss_effective_damage
            
            # 2c. Check for Player Death
            if p_hp_final <= 0:
                continue # Player loses, path discarded

            # ----------------------------------------------------
            # --- 3. Save New State ---
            # ----------------------------------------------------
            
            final_state = (p_hp_final, p_mana_boss_eff, b_hp_boss_eff, 
                           s_timer_boss_eff, p_timer_boss_eff, r_timer_boss_eff)
            
            if new_mana_spent < min_mana_map.get(final_state, float('inf')):
                min_mana_map[final_state] = new_mana_spent
                heapq.heappush(pq, (new_mana_spent,) + final_state)
    
    return min_winning_mana

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting Wizard Battle Solver (Least Mana) using data from: {os.path.abspath(input_file)}\n")
    
    final_score = solve_wizard_battle(input_file)
    
    print("\n" + "="*50)
    print("LEAST AMOUNT OF MANA SPENT TO WIN THE FIGHT:")
    print(f"SCORE: {final_score}")
    print("="*50)