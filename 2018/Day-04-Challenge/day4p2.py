import os
import re
from collections import defaultdict

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def solve_day_4():
    with open(file_path, 'r') as f:
        lines = sorted(f.readlines())

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
            for m in range(sleep_start, minute):
                guard_sleeps[current_guard][m] += 1

    # Strategy 1
    s1_guard = max(guard_sleeps, key=lambda g: sum(guard_sleeps[g]))
    s1_minute = guard_sleeps[s1_guard].index(max(guard_sleeps[s1_guard]))
    
    # Strategy 2
    # We find the guard whose max-minute value is the highest among all guards
    s2_guard = max(guard_sleeps, key=lambda g: max(guard_sleeps[g]))
    s2_minute = guard_sleeps[s2_guard].index(max(guard_sleeps[s2_guard]))

    print(f"Part 1 Answer: {s1_guard * s1_minute}")
    print(f"Part 2 Answer: {s2_guard * s2_minute}")

if __name__ == "__main__":
    solve_day_4()