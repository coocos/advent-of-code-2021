from collections import defaultdict
from pathlib import Path


def parse_input() -> list[int]:
    return [
        int(value)
        for value in (Path(__file__).parent / "input.txt").read_text().split(",")
    ]


def simulate(fish: list[int]) -> list[int]:

    last_gen = [0] * 9
    for timer in fish:
        last_gen[timer] += 1

    days: list[int] = []
    for _ in range(256):
        next_gen = [0] * 9
        for timer, count in enumerate(last_gen):
            if timer != 0:
                next_gen[timer - 1] = count
        next_gen[6] += last_gen[0]
        next_gen[8] += last_gen[0]
        last_gen = next_gen
        days.append(sum(last_gen))

    return days


def solve() -> None:

    fish = parse_input()
    days = simulate(fish)

    # First part
    assert days[79] == 379114

    # Second part
    assert days[255] == 1702631502303


if __name__ == "__main__":
    solve()
