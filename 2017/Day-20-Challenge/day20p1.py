import os
import re
import math
from typing import List, Dict, Tuple

def calculate_magnitude(coords: Tuple[int, int, int]) -> int:
    """Calculates the Manhattan distance magnitude: |X| + |Y| + |Z|."""
    return abs(coords[0]) + abs(coords[1]) + abs(coords[2])

def parse_particles(filepath) -> List[Dict[str, Tuple[int, int, int]]]:
    """
    Reads particle data and extracts coordinates for p, v, and a.
    
    Example input line: p=<-1612,-388,2558>, v=<18,4,-26>, a=<-3,-1,1>
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

    for line in lines:
        match = pattern.match(line)
        if match:
            coords = list(map(int, match.groups()))
            
            particle = {
                'p': tuple(coords[0:3]),
                'v': tuple(coords[3:6]),
                'a': tuple(coords[6:9])
            }
            particles.append(particle)
            
    return particles

def solve_particle_puzzle(filepath):
    """
    Finds the particle index that minimizes the long-term distance based on 
    the (Acceleration, Velocity, Position) magnitude tuple.
    """
    particles = parse_particles(filepath)
    if not particles:
        return -1
        
    min_magnitude_tuple = (float('inf'), float('inf'), float('inf'))
    closest_particle_index = -1
    
    for index, particle in enumerate(particles):
        # 1. Calculate Acceleration Magnitude (M_a) - Primary Key
        M_a = calculate_magnitude(particle['a'])
        
        # 2. Calculate Velocity Magnitude (M_v) - Secondary Key
        M_v = calculate_magnitude(particle['v'])
        
        # 3. Calculate Position Magnitude (M_p) - Tertiary Key
        M_p = calculate_magnitude(particle['p'])
        
        current_magnitude_tuple = (M_a, M_v, M_p)
        
        # Check if the current tuple is lexicographically smaller than the minimum found so far
        if current_magnitude_tuple < min_magnitude_tuple:
            min_magnitude_tuple = current_magnitude_tuple
            closest_particle_index = index
            
    return closest_particle_index

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    print(f"Starting particle long-term stability analysis using data from: {os.path.abspath(input_file)}\n")
    
    final_index = solve_particle_puzzle(input_file)
    
    print("\n" + "="*50)
    print("INDEX OF THE PARTICLE THAT WILL STAY CLOSEST TO <0,0,0>:")
    print(f"SCORE: {final_index}")
    print("="*50)