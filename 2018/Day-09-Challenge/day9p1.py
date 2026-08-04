import os
import re
from collections import deque

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'input.txt')

def play_marble_game(players, last_marble):
    # scores[player_id] = total_score
    scores = [0] * players
    # The circle is represented by a deque for O(1) rotations
    circle = deque([0])
    
    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            # Rule 23:
            # 1. Current player gets current marble value
            player_idx = (marble - 1) % players
            scores[player_idx] += marble
            
            # 2. Rotate 7 times counter-clockwise (rotate right in deque)
            circle.rotate(7)
            
            # 3. Remove that marble and add it to score
            scores[player_idx] += circle.pop()
            
            # 4. The marble clockwise of the removed one is now current
            # Since we popped from the right, the new 'front' is already correct
            circle.rotate(-1)
        else:
            # Normal Rule:
            # Move 1 marble clockwise, then insert (effectively move 2 and insert)
            # In deque terms: rotate left by 1, then append/insert
            circle.rotate(-1)
            circle.append(marble)
            
    return max(scores)

def solve():
    with open(file_path, 'r') as f:
        content = f.read()
        # Extract numbers using regex
        nums = list(map(int, re.findall(r'\d+', content)))
        if len(nums) >= 2:
            players, last_marble = nums[0], nums[1]
            result = play_marble_game(players, last_marble)
            print(f"The winning Elf's score is: {result}")

if __name__ == "__main__":
    solve()