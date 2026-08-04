import os
import sys


def match(rules, rule_id, s, pos, memo):
    key = (rule_id, pos)
    if key in memo:
        return memo[key]
    rule = rules[rule_id]
    ends = set()
    if isinstance(rule, str):
        if pos < len(s) and s[pos] == rule:
            ends.add(pos + 1)
    else:
        for alt in rule:
            cur = {pos}
            for part in alt:
                nxt = set()
                for p in cur:
                    r = match(rules, part, s, p, memo)
                    if r:
                        nxt.update(r)
                cur = nxt
                if not cur:
                    break
            ends.update(cur)
    memo[key] = ends
    return ends


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        data = f.read()

    rules_section, messages_section = data.split('\n\n')
    rules = {}
    for line in rules_section.splitlines():
        rid, body = line.split(': ')
        rid = int(rid)
        if body.startswith('"'):
            rules[rid] = body[1]
        else:
            rules[rid] = [[int(x) for x in alt.split()]
                          for alt in body.split(' | ')]

    # part 2: rule 8 = 42 | 42 8 (one or more 42s)
    # rule 11 = 42 31 | 42 11 31 (n x 42 then n x 31)
    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]

    messages = messages_section.splitlines()

    count = 0
    for m in messages:
        if m and len(m) in match(rules, 0, m, 0, {}):
            count += 1

    print(count)


if __name__ == "__main__":
    main()
