def solve_recipes(num_after):
    # Initial scoreboard and Elf starting indices
    scores = [3, 7]
    elf1 = 0
    elf2 = 1
    
    # We need num_after + 10 recipes to get our final answer
    target_len = num_after + 10
    
    while len(scores) < target_len:
        # Step 1: Combine recipes
        s1 = scores[elf1]
        s2 = scores[elf2]
        recipe_sum = s1 + s2
        
        # Step 2: Add new digits to scoreboard
        if recipe_sum >= 10:
            scores.append(1) # Since max sum is 9+9=18, tens digit is always 1
            scores.append(recipe_sum % 10)
        else:
            scores.append(recipe_sum)
            
        # Step 3: Move Elves
        elf1 = (elf1 + 1 + scores[elf1]) % len(scores)
        elf2 = (elf2 + 1 + scores[elf2]) % len(scores)
        
    # Step 4: Extract the 10 scores after the first 'num_after' entries
    result = "".join(map(str, scores[num_after : num_after + 10]))
    return result

if __name__ == "__main__":
    # Your puzzle input
    puzzle_input = 74501
    print(f"The scores of the ten recipes after {puzzle_input} are: {solve_recipes(puzzle_input)}")