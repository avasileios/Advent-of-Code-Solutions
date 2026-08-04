import collections

class Unit:
    def __init__(self, x, y, u_type, attack_power=3):
        self.x, self.y = x, y
        self.type = u_type  # 'E' or 'G'
        self.hp = 200
        self.attack = attack_power
        self.alive = True

    @property
    def pos(self): return (self.y, self.x) # (row, col) for reading order

def solve_combat(map_str, elf_attack=3):
    lines = map_str.strip().split('\n')
    walls = set()
    units = []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#': walls.add((y, x))
            elif char == 'E': units.append(Unit(x, y, 'E', elf_attack))
            elif char == 'G': units.append(Unit(x, y, 'G'))

    rounds = 0
    while True:
        # 1. Sort units by reading order (y, x)
        units.sort(key=lambda u: u.pos)
        
        full_round_complete = True
        for unit in units:
            if not unit.alive: continue
            
            # Identify current living enemies
            enemies = [u for u in units if u.alive and u.type != unit.type]
            if not enemies:
                full_round_complete = False
                break
            
            # 2. Movement Phase
            if not is_adjacent_to_enemy(unit, enemies):
                move_pos = find_move(unit, enemies, walls, units)
                if move_pos:
                    unit.y, unit.x = move_pos

            # 3. Attack Phase
            attack(unit, enemies)

        if not full_round_complete: break
        
        # Cleanup dead units and increment round
        units = [u for u in units if u.alive]
        rounds += 1

    total_hp = sum(u.hp for u in units if u.alive)
    return rounds * total_hp

def is_adjacent_to_enemy(unit, enemies):
    for e in enemies:
        if abs(unit.y - e.y) + abs(unit.x - e.x) == 1:
            return True
    return False

def find_move(unit, enemies, walls, units):
    occupied = {u.pos for u in units if u.alive and u != unit}
    in_range = set()
    for e in enemies:
        for dy, dx in [(-1,0), (0,-1), (0,1), (1,0)]: # Reading order neighbors
            p = (e.y + dy, e.x + dx)
            if p not in walls and p not in occupied:
                in_range.add(p)
    
    if not in_range: return None

    # BFS to find nearest reachable square
    queue = collections.deque([(unit.pos, 0)])
    visited = {unit.pos}
    dist_map = {}
    found_dist = None
    reachable_targets = []

    while queue:
        curr, d = queue.popleft()
        if found_dist is not None and d > found_dist: break
        if curr in in_range:
            found_dist = d
            reachable_targets.append(curr)
        
        for dy, dx in [(-1,0), (0,-1), (0,1), (1,0)]:
            nxt = (curr[0] + dy, curr[1] + dx)
            if nxt not in walls and nxt not in occupied and nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, d + 1))
    
    if not reachable_targets: return None
    
    # Tie-break destination by reading order
    chosen_dest = min(reachable_targets)

    # BFS from destination back to current pos to find the step
    # To respect reading order of STEP, we check the unit's neighbors
    queue = collections.deque([(chosen_dest, 0)])
    rev_visited = {chosen_dest}
    rev_dist = {chosen_dest: 0}
    while queue:
        curr, d = queue.popleft()
        for dy, dx in [(-1,0), (0,-1), (0,1), (1,0)]:
            nxt = (curr[0] + dy, curr[1] + dx)
            if nxt not in walls and nxt not in occupied and nxt not in rev_visited:
                rev_visited.add(nxt)
                rev_dist[nxt] = d + 1
                queue.append((nxt, d + 1))
    
    # Choose neighbor of unit that is on shortest path and first in reading order
    best_step = None
    min_step_dist = float('inf')
    for dy, dx in [(-1,0), (0,-1), (0,1), (1,0)]:
        step_pos = (unit.y + dy, unit.x + dx)
        if step_pos in rev_dist:
            if rev_dist[step_pos] < min_step_dist:
                min_step_dist = rev_dist[step_pos]
                best_step = step_pos
    return best_step

def attack(unit, enemies):
    adj_enemies = [e for e in enemies if abs(unit.y - e.y) + abs(unit.x - e.x) == 1]
    if not adj_enemies: return
    # Sort by HP (primary) and then Reading Order (secondary)
    target = min(adj_enemies, key=lambda e: (e.hp, e.pos))
    target.hp -= unit.attack
    if target.hp <= 0:
        target.alive = False

# PASTE YOUR INPUT.TXT HERE
raw_input = """################################
##########################.#####
##########################.#####
##########################.#.###
#######################......###
#################....#........##
##############.##....G......G.##
#############..#G...##.........#
#############.GG..G..##.......##
#############.................##
#############G.........G....#.##
###########G..........E........#
###########...#####............#
###########..#######...........#
#######.....#########........###
#######....G#########.......####
##...G.G....#########...#....###
#...G..G...G#########.###E...###
##.......#..#########.#####..E##
#............#######..##########
#.GG........G.#####...##########
#................E.....#########
########..........##.###########
#########.....###.....##########
##########.E..##......##########
#######..#....###.E...##########
######.........###.E############
######.#..G....##..#############
######.....##..##.E#############
#######....##.E...E#############
######....G#......##############
################################"""

if __name__ == "__main__":
    print(f"Battle Outcome: {solve_combat(raw_input)}")