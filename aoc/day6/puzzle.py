from collections import defaultdict
from pathlib import Path


def parse_input() -> list[int]:
    return [
        int(value)
        for value in (Path(__file__).parent / "input.txt").read_text().split(",")
    ]


def solve() -> None:

    fish = {i: 0 for i in range(9)}
    timers = parse_input()
    for timer in timers:
        fish[timer] += 1

    last_gen = fish
    fishes_at_day = {}
    for day in range(256):
        next_gen = defaultdict(int)
        for timer, count in last_gen.items():
            if timer != 0:
                next_gen[timer - 1] = count
        next_gen[6] += last_gen[0]
        next_gen[8] += last_gen[0]
        last_gen = next_gen
        fishes_at_day[day + 1] = sum(last_gen.values())

    # First part
    assert fishes_at_day[80] == 379114

    # Second part
    assert fishes_at_day[256] == 1702631502303


if __name__ == "__main__":
    solve()
