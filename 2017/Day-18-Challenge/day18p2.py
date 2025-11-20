import os
from collections import defaultdict, deque
from typing import List, Dict, Any, Tuple

# --- Constants ---
# Safety limit for steps to avoid runaway simulation
MAX_STEPS = 10_000_000 

def parse_program(filepath) -> List[List[str]]:
    """
    Reads the Duet assembly instructions from the file.
    Returns a list of instruction lists: [opcode, arg1, arg2 (optional)]
    """
    program = []
    try:
        # Robust path reading
        input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filepath)
        with open(input_file, 'r') as f:
            for line in f:
                if line.strip():
                    program.append(line.strip().split())
    except FileNotFoundError:
        print(f"Error: Program file not found at '{filepath}'")
        return []
    return program

def get_value(x_str: str, regs: defaultdict) -> int:
    """
    Helper to get value of register or integer literal.
    """
    try:
        return int(x_str)
    except ValueError:
        return regs[x_str] # Defaults to 0 if register is new/uninitialized

def init_program_state(program_id: int) -> Dict[str, Any]:
    """Initializes the state for one program (registers, IP, queue, etc.)."""
    state = {
        'regs': defaultdict(int),
        'ip': 0,
        'queue': deque(),       # Incoming message queue
        'send_count': 0,        # Tracker for Program 1 (the goal)
        'waiting': False,       # Flag set if program is waiting for rcv
        'terminated': False,    # Flag set if IP goes out of bounds
        'program_id': program_id
    }
    # Register 'p' must start with the program ID
    state['regs']['p'] = program_id
    return state

def execute_step(program: List[List[str]], state: Dict[str, Any], target_queue: deque) -> bool:
    """
    Executes one instruction for the given program state.
    
    Returns:
        bool: True if the program performed an action (moved IP, sent, or received), False if waiting.
    """
    if state['terminated']:
        return False

    ip = state['ip']
    regs = state['regs']
    
    if not (0 <= ip < len(program)):
        state['terminated'] = True
        return False
        
    cmd = program[ip]
    opcode = cmd[0]
    
    # Reset waiting state before execution
    state['waiting'] = False 
    
    # Default IP increment is +1
    ip_increment = 1 
    action_taken = True
    
    # --- Instruction Execution ---
    
    if opcode == 'snd':
        # snd X: sends the value of X to the other program (target_queue).
        X_val = get_value(cmd[1], regs)
        target_queue.append(X_val)
        
        # Track sends for Program 1 only (goal for Part 2)
        if state['program_id'] == 1:
            state['send_count'] += 1
            
    elif opcode == 'set':
        Y_val = get_value(cmd[2], regs)
        regs[cmd[1]] = Y_val
        
    elif opcode == 'add':
        Y_val = get_value(cmd[2], regs)
        regs[cmd[1]] += Y_val
        
    elif opcode == 'mul':
        Y_val = get_value(cmd[2], regs)
        regs[cmd[1]] *= Y_val
        
    elif opcode == 'mod':
        Y_val = get_value(cmd[2], regs)
        if Y_val != 0:
            regs[cmd[1]] %= Y_val
        
    elif opcode == 'rcv':
        # rcv X: stores the next value from its queue in register X.
        if state['queue']:
            received_val = state['queue'].popleft()
            regs[cmd[1]] = received_val
        else:
            # Queue is empty. Program WAITS (does not advance IP).
            state['waiting'] = True
            ip_increment = 0
            action_taken = False
            
    elif opcode == 'jgz':
        X_val = get_value(cmd[1], regs)
        Y_val = get_value(cmd[2], regs)
        
        if X_val > 0:
            ip_increment = Y_val
            
    else:
        # Skip unknown instructions
        pass

    # Update IP only if an action was taken (not waiting)
    if action_taken:
        state['ip'] += ip_increment
        
    return action_taken


def run_concurrent_vms(program):
    """
    Simulates the two programs concurrently until both terminate or deadlock.
    """
    # Initialize states for Program 0 and Program 1
    state_p0 = init_program_state(0)
    state_p1 = init_program_state(1)
    
    # Set of states to monitor for termination/deadlock
    max_steps_safety = MAX_STEPS
    steps = 0
    
    while steps < max_steps_safety:
        steps += 1
        
        # Program 0 tries to execute
        p0_acted = execute_step(program, state_p0, state_p1['queue'])
        
        # Program 1 tries to execute
        p1_acted = execute_step(program, state_p1, state_p0['queue'])
        
        # Check Termination/Deadlock Conditions
        
        # 1. Deadlock: Both are waiting for a value that will never arrive (neither program acted).
        if state_p0['waiting'] and state_p1['waiting']:
            print(f"Deadlock detected after {steps} steps.")
            break
            
        # 2. Termination: Both are terminated.
        if state_p0['terminated'] and state_p1['terminated']:
            print(f"Both programs terminated after {steps} steps.")
            break
            
        # 3. Halt: If no one is terminated, but neither program could execute (e.g., waiting or unknown state)
        if not p0_acted and not p1_acted:
            # If one is waiting and the other is terminated, or if both are waiting, we stop.
            if state_p0['terminated'] or state_p1['terminated'] or (state_p0['waiting'] and state_p1['waiting']):
                break
                
    return state_p1['send_count']

# --- Main Execution Block ---
if __name__ == "__main__":
    # Robust file path construction as requested:
    input_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt")
    
    program_instructions = parse_program(input_file)
    if not program_instructions:
        exit()

    print(f"Starting Concurrent Duet VM simulation (Total instructions: {len(program_instructions)})\n")
    
    final_send_count = run_concurrent_vms(program_instructions)
    
    print("\n" + "="*50)
    print("TOTAL TIMES PROGRAM 1 SENT A VALUE:")
    print(f"SCORE: {final_send_count}")
    print("="*50)