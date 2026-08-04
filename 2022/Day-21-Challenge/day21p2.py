import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")
    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    exprs = {}
    for line in lines:
        name, rest = line.split(': ')
        exprs[name] = rest

    # symbolic evaluation: return (value, depends_on_humn)
    def evaluate(name):
        if name == 'humn':
            return (None, True)
        e = exprs[name]
        parts = e.split()
        if len(parts) == 1:
            return (int(parts[0]), False)
        a, op, b = parts
        va, ha = evaluate(a)
        vb, hb = evaluate(b)
        if not ha and not hb:
            return ({'+': va + vb, '-': va - vb, '*': va * vb, '/': va // vb}[op], False)
        return ((va, op, vb, ha, hb), True)

    root = exprs['root'].split()
    va, ha = evaluate(root[0])
    vb, hb = evaluate(root[2])
    # one side is a value, the other an expression tree containing humn
    if ha:
        target, expr = vb, va
    else:
        target, expr = va, vb

    # walk the expression tree, solving for humn
    while True:
        if expr is None:
            print(target)
            return
        if isinstance(expr, tuple) and expr[0] is None and expr[1] is True:
            print(target)
            return
        val, op, other, h_side, o_side = expr
        # expr = val op other (humn in 'val' side if h_side)
        if h_side:
            # target = val op other  -> solve for val
            if op == '+':
                target = target - other
            elif op == '-':
                target = target + other
            elif op == '*':
                target = target // other
            elif op == '/':
                target = target * other
            expr = val
        else:
            # target = other op val (humn in 'other' side)
            if op == '+':
                target = target - val
            elif op == '-':
                target = val - target
            elif op == '*':
                target = target // val
            elif op == '/':
                target = val // target
            if other is None:
                print(target)
                return
            expr = other


if __name__ == "__main__":
    main()
