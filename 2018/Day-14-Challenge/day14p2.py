def solve_sequence_search(target_str):
    # Convert target string to list of integers for fast comparison
    target = [int(d) for d in target_str]
    target_len = len(target)
    
    scores = [3, 7]
    elf1 = 0
    elf2 = 1
    
    # We'll use a local reference to append for a tiny speed boost
    append = scores.append
    
    while True:
        s1 = scores[elf1]
        s2 = scores[elf2]
        recipe_sum = s1 + s2
        
        # Add recipes and check for match after each individual append
        if recipe_sum >= 10:
            # First digit (1)
            append(1)
            if scores[-target_len:] == target:
                return len(scores) - target_len
            # Second digit
            append(recipe_sum % 10)
            if scores[-target_len:] == target:
                return len(scores) - target_len
        else:
            # Single digit
            append(recipe_sum)
            if scores[-target_len:] == target:
                return len(scores) - target_len
            
        # Move Elves
        elf1 = (elf1 + 1 + s1) % len(scores)
        elf2 = (elf2 + 1 + s2) % len(scores)

if __name__ == "__main__":
    puzzle_input = "074501"
    print(f"Number of recipes to the left of {puzzle_input}: {solve_sequence_search(puzzle_input)}")