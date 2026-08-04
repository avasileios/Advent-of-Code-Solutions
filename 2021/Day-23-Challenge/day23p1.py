import os
import sys
import heapq


COST = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
ROOM_X = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
HALL_STOPS = (0, 1, 3, 5, 7, 9, 10)  # corridor positions where you may stop


def is_done(corridor, rooms):
    if any(c != '.' for c in corridor):
        return False
    for i, room in enumerate(rooms):
        if room != 'ABCD'[i] * len(room):
            return False
    return True


def neighbors(corridor, rooms):
    depth = len(rooms[0])
    # 1) corridor -> room
    for ci, c in enumerate(corridor):
        if c == '.':
            continue
        t = c
        rx = ROOM_X[t]
        ri = ord(t) - ord('A')
        room = rooms[ri]
        # the room must be ready: only same type inside (empty cells ok)
        if any(ch != t and ch != '.' for ch in room):
            continue
        # path from ci to rx must be clear
        step = 1 if rx > ci else -1
        x = ci + step
        clear = True
        while x != rx:
            if corridor[x] != '.':
                clear = False
                break
            x += step
        if not clear:
            continue
        # move into the room: as deep as possible
        target_idx = depth - 1 - room.count(t)
        if target_idx < 0:
            continue
        dist = abs(rx - ci) + target_idx + 1
        new_corridor = corridor[:ci] + '.' + corridor[ci + 1:]
        new_room = room[:target_idx] + t + room[target_idx + 1:]
        new_rooms = rooms[:ri] + (new_room,) + rooms[ri + 1:]
        yield new_corridor, new_rooms, dist * COST[t]
    # 2) room -> corridor
    for ri, room in enumerate(rooms):
        t = 'ABCD'[ri]
        # find the topmost amphipod
        top = None
        for idx, ch in enumerate(room):
            if ch != '.':
                top = (idx, ch)
                break
        if top is None:
            continue
        idx, ch = top
        # if the room contains only correct amphipods below/at top, they stay
        if all(c == t for c in room[idx:]):
            continue
        rx = ROOM_X[t]
        rx = ROOM_X[t]
        for hx in HALL_STOPS:
            if corridor[hx] != '.':
                continue
            # path clear?
            step = 1 if hx > rx else -1
            x = rx + step
            clear = True
            while x != hx:
                if corridor[x] != '.':
                    clear = False
                    break
                x += step
            if not clear:
                continue
            dist = abs(hx - rx) + idx + 1
            new_corridor = corridor[:hx] + ch + corridor[hx + 1:]
            new_room = room[:idx] + '.' + room[idx + 1:]
            new_rooms = rooms[:ri] + (new_room,) + rooms[ri + 1:]
            yield new_corridor, new_rooms, dist * COST[ch]


def solve(corridor, rooms):
    start = (corridor, rooms)
    dist = {start: 0}
    pq = [(0, start)]
    while pq:
        d, state = heapq.heappop(pq)
        if dist.get(state, 10**18) != d:
            continue
        corr, rms = state
        if is_done(corr, rms):
            return d
        for nc, nr, nd in neighbors(corr, rms):
            nstate = (nc, nr)
            nd2 = d + nd
            if nd2 < dist.get(nstate, 10**18):
                dist[nstate] = nd2
                heapq.heappush(pq, (nd2, nstate))
    return None


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    room_rows = []
    for line in lines:
        if line.startswith('#'):
            pass
        if '#' in line and line.strip().startswith('#'):
            room_rows.append(line)
    # room_rows[0] = "#############", skip; the actual room rows contain
    # letters
    room_rows = [line for line in room_rows if any(c in 'ABCD' for c in line)]

    rooms = ['', '', '', '']
    for row in room_rows:
        for i, room in enumerate('ABCD'):
            c = row[3 + i * 2]
            if c in 'ABCD':
                rooms[i] += c
    rooms = tuple(rooms)
    corridor = '.' * 11

    print(solve(corridor, rooms))


if __name__ == "__main__":
    main()
