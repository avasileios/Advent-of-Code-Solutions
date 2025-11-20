import os
import re

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "input.txt"), "r") as file:
    corrupted_memory = file.read()

pattern = r"mul\((\d{1,3}),(\d{1,3})\)" #Grouping

matches = re.findall(pattern,corrupted_memory)
#print(matches)

result_sum = 0
for x,y in matches:
    result_sum += int(x) * int(y)
print(result_sum)

# Time O(n + m) so O(n)
# Space O(m)
# LINEAR!!!!