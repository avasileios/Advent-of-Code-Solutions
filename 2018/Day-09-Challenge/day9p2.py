import os
import re
from collections import deque

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def play_marble_game(players, last_marble):
    scores = [0] * players
    circle = deque([0])
    
    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            player_idx = (marble - 1) % players
            scores[player_idx] += marble
            
            # Rotate 7 times counter-clockwise
            circle.rotate(7)
            scores[player_idx] += circle.pop()
            
            # The marble clockwise of the removed one becomes current
            circle.rotate(-1)
        else:
            # Move 1 clockwise, then insert (rotate left by 1)
            circle.rotate(-1)
            circle.append(marble)
            
    return max(scores)

def solve():
    with open(file_path, 'r') as f:
        content = f.read()
        nums = list(map(int, re.findall(r'\d+', content)))
        if len(nums) >= 2:
            players, last_marble = nums[0], nums[1]
            
            # Part 2: Multiply the last marble value by 100
            new_last_marble = last_marble * 100
            
            result = play_marble_game(players, new_last_marble)
            print(f"The new winning Elf's score is: {result}")

if __name__ == "__main__":
    solve()