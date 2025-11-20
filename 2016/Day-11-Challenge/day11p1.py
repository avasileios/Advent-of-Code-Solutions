import os
from collections import deque
import re
from itertools import combinations
from typing import Tuple, Dict, Set, List, Any

# --- Constants ---
NUM_FLOORS = 4
GOAL_FLOOR = NUM_FLOORS - 1 # 3 (index of F4)

# Item Type representation: (0-indexed item type, 'G' or 'M')
# Item Types: 0=Promethium, 1=Cobalt, 2=Curium, 3=Ruthenium, 4=Plutonium

def get_hardcoded_initial_state():
    """
    Returns the initial state based on the user's hardcoded input.
    """
    
    # Floor 0 (F1): Promethium Generator (0, G), Promethium Microchip (0, M)
    floor0 = frozenset([(0, 'G'), (0, 'M')])
    
    # Floor 1 (F2): CoG (1, G), CmG (2, G), RuG (3, G), PuG (4, G)
    floor1 = frozenset([(1, 'G'), (2, 'G'), (3, 'G'), (4, 'G')])
    
    # Floor 2 (F3): CoM (1, M), CmM (2, M), RuM (3, M), PuM (4, M)
    floor2 = frozenset([(1, 'M'), (2, 'M'), (3, 'M'), (4, 'M')])
    
    # Floor 3 (F4): Nothing relevant
    floor3 = frozenset()
    
    initial_floors_raw_frozenset = (floor0, floor1, floor2, floor3)
    item_types = ["Promethium", "Cobalt", "Curium", "Ruthenium", "Plutonium"]

    return (0, initial_floors_raw_frozenset), item_types


def is_safe(floor_items: Set[Tuple[int, str]]) -> bool:
    """
    Checks the safety rule for a single floor: 
    If a generator Gx is present, all microchips My must be paired with Gy.
    """
    present_generators = {idx for idx, type in floor_items if type == 'G'}
    
    # If no generators, all chips are safe
    if not present_generators:
        return True
        
    present_microchips = {idx for idx, type in floor_items if type == 'M'}
    
    # Check if any UNPAIRED chip is present alongside a foreign generator.
    # Chip M_y is fried if: (Chip M_y is present) AND (M_y's own generator G_y is NOT present) 
    # AND (at least one other generator G_x is present).
    for chip_idx in present_microchips:
        if chip_idx not in present_generators and len(present_generators) > 0:
            return False
            
    return True


def get_all_next_states(current_state: Tuple[int, Tuple], ROWS: int, item_types: List[str], canonical_to_raw_map: Dict) -> List[Tuple[Tuple, Tuple]]:
    """
    Generates all valid, safe next states from the current state.
    
    Returns:
        list of (canonical_next_state, new_floors_raw_tuple)
    """
    current_floor, current_canonical_items = current_state
    
    # Get the raw floor state needed for generating moves
    current_floors_raw_frozenset = canonical_to_raw_map[current_state]
    current_floors_raw = [set(f) for f in current_floors_raw_frozenset]

    items_on_current_floor = current_floors_raw[current_floor]
    
    possible_next_states = []
    
    # 1. Determine possible elevator movement direction (Up, Down)
    possible_moves = []
    if current_floor < ROWS - 1: possible_moves.append(1) # Up
    if current_floor > 0: possible_moves.append(-1) # Down
        
    
    # 2. Determine possible item loads (1 or 2 items)
    items_to_move = list(combinations(items_on_current_floor, 1)) + \
                    list(combinations(items_on_current_floor, 2))
    
    # 3. Generate new states by trying every move (Up/Down) with every load (1/2 items)
    for direction in possible_moves:
        next_floor = current_floor + direction
        
        # --- Pruning Optimization Check ---
        # Optimization: Only move down if there are items below the destination floor.
        if direction == -1:
             # Check if all floors below the current floor are empty. If so, don't move down.
             is_any_item_below = any(len(current_floors_raw[f]) > 0 for f in range(next_floor))
             
             # Also check if the destination floor is empty. If it is, the move is likely useless.
             is_destination_empty = not current_floors_raw[next_floor]
             
             if not is_any_item_below and is_destination_empty:
                 continue 

        
        for load in items_to_move:
            
            # --- Generate RAW Next State ---
            raw_floors = [f.copy() for f in current_floors_raw] 
            
            # Remove load from current floor
            new_current_floor_items = items_on_current_floor.difference(set(load))
            
            # Add load to next floor
            new_next_floor_items = raw_floors[next_floor].union(set(load))
            
            # Safety Check 1: Check safety of the CURRENT floor AFTER removal
            if not is_safe(new_current_floor_items): continue
                
            # Safety Check 2: Check safety of the DESTINATION floor AFTER addition
            if not is_safe(new_next_floor_items): continue
                
            # --- Build Canonical State ---
            
            raw_floors[current_floor] = frozenset(new_current_floor_items)
            raw_floors[next_floor] = frozenset(new_next_floor_items)
            
            # Now, find the canonical representation of this new raw state
            new_floors_raw_tuple = tuple(raw_floors)
            
            new_item_locations = {}
            for item_idx in range(len(item_types)):
                g_floor = -1
                m_floor = -1
                
                for floor_idx, f_items in enumerate(new_floors_raw_tuple):
                    if (item_idx, 'G') in f_items: g_floor = floor_idx
                    if (item_idx, 'M') in f_items: m_floor = floor_idx
                        
                canonical_item_tuple = (g_floor, m_floor)
                new_item_locations[item_idx] = canonical_item_tuple
                
            canonical_item_tuple = tuple(sorted(new_item_locations.values()))
            canonical_next_state = (next_floor, canonical_item_tuple)
            
            possible_next_states.append((canonical_next_state, new_floors_raw_tuple))
            
    return possible_next_states


def solve_rtg_facility(filepath=None):
    """
    Uses BFS with canonicalization to find the minimum number of steps to move 
    all items to the top floor.
    """
    # 1. Setup Initial and Goal States (using hardcoded input)
    initial_state_tuple_raw, item_types = get_hardcoded_initial_state()
    initial_elevator, initial_floors_raw_frozenset = initial_state_tuple_raw
    
    # Generate canonical initial state
    initial_item_locations = {}
    for item_idx in range(len(item_types)):
        g_floor = -1
        m_floor = -1
        for floor_idx, f_items in enumerate(initial_floors_raw_frozenset):
            if (item_idx, 'G') in f_items: g_floor = floor_idx
            if (item_idx, 'M') in f_items: m_floor = floor_idx
        initial_item_locations[item_idx] = (g_floor, m_floor)
        
    canonical_initial_item_tuple = tuple(sorted(initial_item_locations.values()))
    canonical_initial_state = (initial_elevator, canonical_initial_item_tuple)


    # Goal state: All components are on the top floor.
    goal_pair = (GOAL_FLOOR, GOAL_FLOOR)
    num_item_pairs = len(item_types)
    canonical_goal_item_tuple = tuple([goal_pair] * num_item_pairs)
    canonical_goal_state = (GOAL_FLOOR, canonical_goal_item_tuple)
    
    print(f"Number of item pairs: {num_item_pairs}")
    print(f"Goal state: E={GOAL_FLOOR + 1}, Items={canonical_goal_item_tuple}")

    # 2. BFS Initialization
    # Queue stores: (canonical_state, steps)
    queue = deque([(canonical_initial_state, 0)]) 
    visited = {canonical_initial_state}
    
    # Map from canonical state to the raw floor configuration (for safety checks/next move generation)
    canonical_to_raw_map = {canonical_initial_state: initial_floors_raw_frozenset}

    # 3. BFS Loop
    while queue:
        current_state_canonical, steps = queue.popleft()
        
        # Check for goal
        if current_state_canonical == canonical_goal_state:
            return steps
            
        # Generate next states
        # The generator function returns (canonical_next_state, new_floors_raw_tuple)
        
        for canonical_next_state, new_floors_raw_tuple in get_all_next_states(
            current_state_canonical, NUM_FLOORS, item_types, canonical_to_raw_map
        ):
            
            # 4. Enqueue if unvisited
            if canonical_next_state not in visited:
                visited.add(canonical_next_state)
                # Store the raw floor state for the next move generation
                canonical_to_raw_map[canonical_next_state] = tuple(frozenset(f) for f in new_floors_raw_tuple)
                queue.append((canonical_next_state, steps + 1))
                    
    return -1 # Goal unreachable


# --- Main Execution Block ---
if __name__ == "__main__":
    
    print(f"Starting Radioisotope Facility BFS search (Target F{GOAL_FLOOR + 1}) with hardcoded 5-pair input.\n")
    
    final_steps = solve_rtg_facility()
    
    print("\n" + "="*50)
    print("MINIMUM NUMBER OF STEPS REQUIRED TO BRING ALL OBJECTS TO F4:")
    print(f"SCORE: {final_steps}")
    print("="*50)