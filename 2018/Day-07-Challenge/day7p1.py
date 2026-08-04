import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def solve_step_order(path):
    # adj[A] = [B, D] means A must be done before B and D
    adj = {}
    # in_degree[B] = 2 means B has 2 prerequisites
    in_degree = {}
    all_steps = set()

    with open(path, 'r') as f:
        for line in f:
            # Format: "Step C must be finished before step A can begin."
            match = re.search(r'Step ([A-Z]) must be finished before step ([A-Z])', line)
            if match:
                pre, post = match.groups()
                
                if pre not in adj: adj[pre] = []
                adj[pre].append(post)
                
                in_degree[post] = in_degree.get(post, 0) + 1
                if pre not in in_degree: in_degree[pre] = 0
                
                all_steps.add(pre)
                all_steps.add(post)

    # Find initial available steps (those with in-degree 0)
    available = [s for s in all_steps if in_degree.get(s, 0) == 0]
    result = []

    while available:
        available.sort() # Ensure alphabetical order
        current = available.pop(0)
        result.append(current)

        # "Unlock" the next steps
        if current in adj:
            for neighbor in adj[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    available.append(neighbor)

    return "".join(result)

if __name__ == "__main__":
    order = solve_step_order(file_path)
    print(f"The correct order of steps is: {order}")