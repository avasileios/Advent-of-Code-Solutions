import re
import os
import copy

class Group:
    def __init__(self, army_type, id, units, hp, mods, dmg, dmg_type, init):
        self.army_type = army_type
        self.id = id
        self.units = units
        self.hp = hp
        self.dmg = dmg
        self.dmg_type = dmg_type
        self.init = init
        self.weaknesses = mods.get('weak', [])
        self.immunities = mods.get('immune', [])
        self.target = None

    @property
    def effective_power(self):
        return self.units * self.dmg

    def calculate_damage_to(self, defender):
        if self.dmg_type in defender.immunities:
            return 0
        damage = self.effective_power
        if self.dmg_type in defender.weaknesses:
            damage *= 2
        return damage

def parse_input():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'input.txt')
    with open(file_path, 'r') as f:
        content = f.read().split('\n\n')

    original_groups = []
    for section in content:
        lines = section.strip().split('\n')
        army_name = lines[0].replace(':', '')
        for i, line in enumerate(lines[1:]):
            main = re.match(r"(\d+) units each with (\d+) hit points (.*)with an attack that does (\d+) (\w+) damage at initiative (\d+)", line)
            units, hp, mod_str, dmg, dmg_type, init = main.groups()
            mods = {}
            if '(' in mod_str:
                parts = mod_str.strip("() ").split('; ')
                for p in parts:
                    m = re.match(r"(weak|immune) to (.*)", p)
                    mods[m.group(1)] = m.group(2).split(', ')
            original_groups.append(Group(army_name, i+1, int(units), int(hp), mods, int(dmg), dmg_type, int(init)))
    return original_groups

def run_battle(original_groups, boost):
    # Deep copy to keep original data intact
    groups = copy.deepcopy(original_groups)
    for g in groups:
        if g.army_type == "Immune System":
            g.dmg += boost

    while len(set(g.army_type for g in groups)) > 1:
        # 1. Target Selection
        groups.sort(key=lambda x: (x.effective_power, x.init), reverse=True)
        for g in groups: g.target = None
        targeted = set()
        for attacker in groups:
            enemies = [g for g in groups if g.army_type != attacker.army_type and g not in targeted]
            if not enemies: continue
            enemies.sort(key=lambda e: (attacker.calculate_damage_to(e), e.effective_power, e.init), reverse=True)
            best_enemy = enemies[0]
            if attacker.calculate_damage_to(best_enemy) > 0:
                attacker.target = best_enemy
                targeted.add(best_enemy)

        # 2. Attacking
        groups.sort(key=lambda x: x.init, reverse=True)
        total_killed = 0
        for attacker in groups:
            if attacker.units <= 0 or not attacker.target: continue
            damage = attacker.calculate_damage_to(attacker.target)
            units_killed = min(attacker.target.units, damage // attacker.target.hp)
            attacker.target.units -= units_killed
            total_killed += units_killed
        
        groups = [g for g in groups if g.units > 0]
        if total_killed == 0: # Stalemate detected
            return "Infection", 0
            
    winner = groups[0].army_type
    return winner, sum(g.units for g in groups)

def solve():
    original_groups = parse_input()
    
    # Simple binary search for the smallest boost
    low = 0
    high = 100000 
    ans = 0

    while low <= high:
        mid = (low + high) // 2
        winner, units = run_battle(original_groups, mid)
        
        if winner == "Immune System":
            ans = units
            high = mid - 1 # Try to find a smaller boost
        else:
            low = mid + 1 # Need more power
            
    return ans

if __name__ == "__main__":
    result = solve()
    print(f"Remaining units with smallest required boost: {result}")