import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        data = f.read()

    required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
    valid = 0
    for passport in data.split('\n\n'):
        fields = {}
        for token in passport.split():
            k, v = token.split(':')
            fields[k] = v
        if required <= set(fields):
            valid += 1

    print(valid)


if __name__ == "__main__":
    main()
