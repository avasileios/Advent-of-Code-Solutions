import os
import re

# The total duration of the race in seconds
RACE_DURATION = 2503

def parse_reindeer_data(filepath):
    """
    Reads the input and extracts the parameters for each reindeer.
    
    Returns:
        list: A list of dictionaries, one for each reindeer.
    """
    reindeer_data = []
    
    try:
        # Robust path reading
        with open(filepath, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Instructions file not found at '{filepath}'")
        return []
    
    # Regex to capture: Name, speed, fly_time, rest_time
    # Example: Vixen can fly 19 km/s for 7 seconds, but then must rest for 124 seconds.
    pattern = re.compile(
        r'(\w+)\s+can fly\s+(\d+)\s+km/s for\s+(\d+)\s+seconds, but then must rest for\s+(\d+)\s+seconds\.'
    )
    
    for line in lines:
        match = pattern.match(line)
        if not match:
            continue
            
        name, speed_str, fly_time_str, rest_time_str = match.groups()
        
        reindeer_data.append({
            'name': name,
            'speed': int(speed_str),
            'fly_time': int(fly_time_str),
            'rest_time': int(rest_time_str)
        })
        
    return reindeer_data

def solve_reindeer_race_p1(filepath):
    """
    Simulates the race second-by-second and determines the distance of the 
    winning reindeer after RACE_DURATION seconds.
    """
    reindeer_params = parse_reindeer_data(filepath)
    if not reindeer_params:
        print("No reindeer data parsed.")
        return 0
        
    # Initialize state for each reindeer
    reindeer_states = {}
    for p in reindeer_params:
        reindeer_states[p['name']] = {
            'distance': 0,
            'time_in_state': 0, # Time spent in the current state (flying or resting)
            'is_flying': True, # Start flying
            'params': p
        }

    # --- Simulation Loop ---
    for _ in range(1, RACE_DURATION + 1):
        for name, state in reindeer_states.items():
            params = state['params']
            
            # 1. Update Distance
            if state['is_flying']:
                state['distance'] += params['speed']
            
            # 2. Advance time in current state
            state['time_in_state'] += 1
            
            # 3. Check for state transition
            if state['is_flying']:
                if state['time_in_state'] == params['fly_time']:
                    # Transition from flying to resting
                    state['is_flying'] = False
                    state['time_in_state'] = 0
            else: # is resting
                if state['time_in_state'] == params['rest_time']:
                    # Transition from resting to flying
                    state['is_flying'] = True
                    state['time_in_state'] = 0

    # Find the maximum distance traveled
    winning_distance = max(state['distance'] for state in reindeer_states.values())
    
    return winning_distance

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting Reindeer Race simulation for {RACE_DURATION} seconds using data from: {os.path.abspath(input_file)}\n")
    
    final_score = solve_reindeer_race_p1(input_file)
    
    print("\n" + "="*50)
    print("DISTANCE TRAVELED BY THE WINNING REINDEER:")
    print(f"SCORE: {final_score}")
    print("="*50)