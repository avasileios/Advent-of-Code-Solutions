import os
import re
from collections import defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def solve_guard_strategy_1(path):
    with open(path, 'r') as f:
        lines = sorted(f.readlines()) # Step 1: Sort chronologically

    # guard_sleeps[guard_id] = [0, 0, ... 0] (60 zeros for 60 minutes)
    guard_sleeps = defaultdict(lambda: [0] * 60)
    
    current_guard = None
    sleep_start = 0

    for line in lines:
        minute = int(re.search(r':(\d+)', line).group(1))
        
        if "Guard" in line:
            current_guard = int(re.search(r'#(\d+)', line).group(1))
        elif "falls asleep" in line:
            sleep_start = minute
        elif "wakes up" in line:
            # Increment every minute the guard was asleep
            for m in range(sleep_start, minute):
                guard_sleeps[current_guard][m] += 1

    # Strategy 1: Find guard with most total minutes asleep
    sleepiest_guard = max(guard_sleeps, key=lambda g: sum(guard_sleeps[g]))
    
    # Find which minute that guard was asleep most often
    minutes_list = guard_sleeps[sleepiest_guard]
    peak_minute = minutes_list.index(max(minutes_list))
    
    return sleepiest_guard * peak_minute

if __name__ == "__main__":
    result = solve_guard_strategy_1(file_path)
    print(f"Strategy 1 Result (ID * Minute): {result}")