import os

# Path setup
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def react_polymer(polymer):
    stack = []
    
    for unit in polymer:
        if stack:
            # Check if units react:
            # 1. They are the same letter: unit.lower() == stack[-1].lower()
            # 2. They have different polarity: unit != stack[-1]
            if unit.lower() == stack[-1].lower() and unit != stack[-1]:
                stack.pop()
                continue
        
        stack.append(unit)
    
    return len(stack)

if __name__ == "__main__":
    try:
        with open(file_path, 'r') as f:
            # .strip() is vital to remove the trailing newline character
            data = f.read().strip()
        
        remaining_units = react_polymer(data)
        print(f"Number of units remaining: {remaining_units}")
    except FileNotFoundError:
        print("Error: input.txt not found.")