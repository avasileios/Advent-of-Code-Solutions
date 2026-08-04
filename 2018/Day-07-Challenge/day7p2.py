import os
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def get_duration(step):
    # ord('A') is 65. We want A=1, so 65 - 64 = 1.
    # Total time is 60 + letter_value.
    return 60 + (ord(step) - 64)

def solve_multitasking(path, num_workers=5):
    adj = {}
    in_degree = {}
    all_steps = set()

    with open(path, 'r') as f:
        for line in f:
            match = re.search(r'Step ([A-Z]) must be finished before step ([A-Z])', line)
            if match:
                pre, post = match.groups()
                adj.setdefault(pre, []).append(post)
                in_degree[post] = in_degree.get(post, 0) + 1
                if pre not in in_degree: in_degree[pre] = 0
                all_steps.update([pre, post])

    # steps_to_do: steps whose prerequisites are finished
    available = sorted([s for s in all_steps if in_degree.get(s, 0) == 0])
    
    # workers: list of [step_letter, seconds_remaining]
    workers = [[None, 0] for _ in range(num_workers)]
    
    total_seconds = 0
    completed_count = 0
    total_steps = len(all_steps)

    while completed_count < total_steps:
        # 1. Assign tasks to idle workers
        for i in range(num_workers):
            if workers[i][0] is None and available:
                task = available.pop(0)
                workers[i] = [task, get_duration(task)]

        # 2. Find the shortest time any worker has left to finish their current task
        # This speeds up the simulation instead of ticking 1 second at a time
        active_times = [w[1] for w in workers if w[0] is not None]
        time_step = min(active_times) if active_times else 1
        
        total_seconds += time_step

        # 3. Work on tasks and finish them
        for i in range(num_workers):
            if workers[i][0] is not None:
                workers[i][1] -= time_step
                
                # If task is finished this tick
                if workers[i][1] == 0:
                    finished_task = workers[i][0]
                    workers[i][0] = None
                    completed_count += 1
                    
                    # Unlock dependent steps
                    if finished_task in adj:
                        for neighbor in adj[finished_task]:
                            in_degree[neighbor] -= 1
                            if in_degree[neighbor] == 0:
                                available.append(neighbor)
        
        # Keep available steps alphabetical for the next worker assignment
        available.sort()

    return total_seconds

if __name__ == "__main__":
    result = solve_multitasking(file_path)
    print(f"Total time to complete with 5 workers: {result} seconds")