import os
import re
from typing import List, Dict, Tuple, Any
from collections import defaultdict

# --- Simulation Constants ---
# Ticks without collision required to confirm stabilization
STABILITY_WINDOW = 500 

def parse_particles(filepath) -> List[Dict[str, Tuple[int, int, int]]]:
    """
    Reads particle data and extracts initial p, v, and a vectors.
    """
    particles = []
    
    # Regex to capture all 9 integer coordinates (x, y, z for p, v, a)
    pattern = re.compile(
        r'p=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>,\s*'
        r'v=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>,\s*'
        r'a=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>'
    )
    
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: Particle data file not found at '{filepath}'")
        return []

    for index, line in enumerate(lines):
        match = pattern.match(line)
        if match:
            coords = list(map(int, match.groups()))
            
            particle = {
                'id': index,
                'p': list(coords[0:3]), # Use list for mutability
                'v': list(coords[3:6]),
                'a': list(coords[6:9])
            }
            particles.append(particle)
            
    return particles

def update_particle(p: Dict[str, Any]):
    """
    Updates a particle's velocity and position for one tick.
    """
    # 1. Update velocity by acceleration
    for i in range(3):
        p['v'][i] += p['a'][i]
        
    # 2. Update position by new velocity
    for i in range(3):
        p['p'][i] += p['v'][i]

def solve_collision_puzzle(filepath):
    """
    Simulates particle movement until all collisions are resolved and the system stabilizes.
    """
    active_particles = parse_particles(filepath)
    if not active_particles:
        return 0

    ticks = 0
    ticks_since_last_collision = 0
    
    print(f"Starting with {len(active_particles)} particles.")
    print(f"Stabilization requires {STABILITY_WINDOW} ticks without collision.")

    # --- Simulation Loop ---
    while ticks_since_last_collision < STABILITY_WINDOW:
        
        # 1. Update all active particles
        for p in active_particles:
            update_particle(p)
            
        # 2. Check for collisions
        # Map: position_tuple -> list_of_colliding_particles
        position_map = defaultdict(list)
        
        for p in active_particles:
            # Use tuple of position (px, py, pz) as the hashable key
            position_tuple = tuple(p['p'])
            position_map[position_tuple].append(p)
            
        # 3. Identify and remove collisions
        colliding_ids = set()
        
        for pos, particles_at_pos in position_map.items():
            if len(particles_at_pos) >= 2:
                # Collision occurred at this position
                for p in particles_at_pos:
                    colliding_ids.add(p['id'])
        
        if colliding_ids:
            # Remove colliding particles
            active_particles = [p for p in active_particles if p['id'] not in colliding_ids]
            ticks_since_last_collision = 0 # Reset stability counter
            print(f"Tick {ticks}: {len(colliding_ids)} particles collided. {len(active_particles)} remaining.")
        else:
            ticks_since_last_collision += 1
            
        ticks += 1
        
        # Safety break for extremely long simulations
        if ticks > 1000000:
             print("Safety break: Too many ticks without stabilization.")
             break

    return len(active_particles)

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting collision resolution simulation using data from: {os.path.abspath(input_file)}\n")
    
    final_count = solve_collision_puzzle(input_file)
    
    print("\n" + "="*50)
    print("TOTAL NUMBER OF PARTICLES LEFT AFTER ALL COLLISIONS ARE RESOLVED:")
    print(f"SCORE: {final_count}")
    print("="*50)