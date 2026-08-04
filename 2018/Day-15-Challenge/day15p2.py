import collections

class Unit:
    def __init__(self, x, y, u_type, attack_power):
        self.x, self.y = x, y
        self.type = u_type
        self.hp = 200
        self.attack = attack_power
        self.alive = True

    @property
    def pos(self): return (self.y, self.x)

def simulate(map_str, elf_power):
    lines = map_str.strip().split('\n')
    walls = set()
    units = []
    initial_elf_count = 0
    
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == '#': walls.add((y, x))
            elif char == 'E': 
                units.append(Unit(x, y, 'E', elf_power))
                initial_elf_count += 1
            elif char == 'G': 
                units.append(Unit(x, y, 'G', 3))

    rounds = 0
    while True:
        units.sort(key=lambda u: u.pos)
        full_round = True
        
        for unit in units:
            if not unit.alive: continue
            
            enemies = [u for u in units if u.alive and u.type != unit.type]
            if not enemies:
                full_round = False
                break
            
            # Move if not in range
            if not any(abs(unit.y - e.y) + abs(unit.x - e.x) == 1 for e in enemies):
                move_pos = find_move(unit, enemies, walls, units)
                if move_pos:
                    unit.y, unit.x = move_pos

            # Attack
            adj_enemies = [e for e in enemies if abs(unit.y - e.y) + abs(unit.x - e.x) == 1]
            if adj_enemies:
                target = min(adj_enemies, key=lambda e: (e.hp, e.pos))
                target.hp -= unit.attack
                if target.hp <= 0:
                    target.alive = False
                    # IMMEDIATE FAILURE: If an Elf dies, this power level is invalid
                    if target.type == 'E':
                        return None, None 

        if not full_round: break
        units = [u for u in units if u.alive]
        rounds += 1

    total_hp = sum(u.hp for u in units if u.alive)
    return rounds, total_hp

def find_move(unit, enemies, walls, units):
    occupied = {u.pos for u in units if u.alive and u != unit}
    in_range = set()
    for e in enemies:
        for dy, dx in [(-1,0), (0,-1), (0,1), (1,0)]:
            p = (e.y + dy, e.x + dx)
            if p not in walls and p not in occupied: in_range.add(p)
    if not in_range: return None

    queue = collections.deque([(unit.pos, 0)])
    visited = {unit.pos}
    reachable = []
    found_dist = None

    while queue:
        curr, d = queue.popleft()
        if found_dist is not None and d > found_dist: break
        if curr in in_range:
            found_dist = d
            reachable.append(curr)
        for dy, dx in [(-1,0), (0,-1), (0,1), (1,0)]:
            nxt = (curr[0] + dy, curr[1] + dx)
            if nxt not in walls and nxt not in occupied and nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, d + 1))
    
    if not reachable: return None
    chosen_dest = min(reachable)

    # Find the best step via reverse BFS
    queue = collections.deque([(chosen_dest, 0)])
    rev_dist = {chosen_dest: 0}
    while queue:
        curr, d = queue.popleft()
        for dy, dx in [(-1,0), (0,-1), (0,1), (1,0)]:
            nxt = (curr[0] + dy, curr[1] + dx)
            if nxt not in walls and nxt not in occupied and nxt not in rev_dist:
                rev_dist[nxt] = d + 1
                queue.append((nxt, d + 1))
    
    for dy, dx in [(-1,0), (0,-1), (0,1), (1,0)]:
        step_pos = (unit.y + dy, unit.x + dx)
        if step_pos in rev_dist and rev_dist[step_pos] == found_dist - 1:
            return step_pos
    return None

# --- Main Search Loop ---
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

power = 4
while True:
    rounds, hp_sum = simulate(raw_input, power)
    if rounds is not None:
        print(f"Elves win with {power} attack power.")
        print(f"Outcome: {rounds} * {hp_sum} = {rounds * hp_sum}")
        break
    power += 1