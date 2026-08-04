import os
import sys
import re


def valid_field(k, v):
    if k == 'byr':
        return 1920 <= int(v) <= 2002 if v.isdigit() else False
    if k == 'iyr':
        return 2010 <= int(v) <= 2020 if v.isdigit() else False
    if k == 'eyr':
        return 2020 <= int(v) <= 2030 if v.isdigit() else False
    if k == 'hgt':
        m = re.fullmatch(r'(\d+)(cm|in)', v)
        if not m:
            return False
        num, unit = int(m.group(1)), m.group(2)
        return (150 <= num <= 193) if unit == 'cm' else (59 <= num <= 76)
    if k == 'hcl':
        return re.fullmatch(r'#[0-9a-f]{6}', v) is not None
    if k == 'ecl':
        return v in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
    if k == 'pid':
        return re.fullmatch(r'\d{9}', v) is not None
    if k == 'cid':
        return True
    return False


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
        if required <= set(fields) and all(valid_field(k, v)
                                           for k, v in fields.items()):
            valid += 1

    print(valid)


if __name__ == "__main__":
    main()
