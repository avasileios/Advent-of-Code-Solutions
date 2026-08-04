import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]

    n = 119315717514047
    repeats = 101741582076661

    # each technique is a linear function f(x) = a*x + b (mod n); compose
    # them all into F(x) = A*x + B
    A, B = 1, 0
    for line in lines:
        parts = line.split()
        if line.startswith('deal into new stack'):
            a, b = n - 1, n - 1
        elif line.startswith('cut'):
            k = int(parts[-1]) % n
            a, b = 1, (n - k) % n
        elif line.startswith('deal with increment'):
            k = int(parts[-1]) % n
            a, b = k, 0
        # compose: new_f = f(g(x)) where g is current (A,B) applied first
        # F(x) = a*(A*x + B) + b = a*A*x + a*B + b
        A, B = (a * A) % n, (a * B + b) % n

    # F^k(x) = A^k * x + B * (A^k - 1) / (A - 1)
    def inv(v):
        return pow(v, n - 2, n)

    Ak = pow(A, repeats, n)
    # find x so that F^k(x) = 2020:
    # A^k * x + B*(A^k-1)/(A-1) = 2020
    if A == 1:
        # B * k + x = 2020
        x = (2020 - B * repeats) % n
    else:
        const = (B * (Ak - 1) % n) * inv(A - 1) % n
        x = ((2020 - const) % n) * inv(Ak) % n

    print(x)


if __name__ == "__main__":
    main()
