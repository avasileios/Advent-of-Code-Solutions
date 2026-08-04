import os
import sys


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "input.txt")

    with open(input_file, 'r') as f:
        card_pk, door_pk = (int(x) for x in f.read().split())

    # find the card's loop size
    subject = 7
    value = 1
    loop = 0
    while value != card_pk:
        value = (value * subject) % 20201227
        loop += 1

    # transform the door's public key by the card's loop size
    value = 1
    for _ in range(loop):
        value = (value * door_pk) % 20201227

    print(value)


if __name__ == "__main__":
    main()
