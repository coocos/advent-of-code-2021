import functools
from typing import Iterator
from pathlib import Path


def parse_input() -> list[int]:

    lines = (Path(__file__).parent / "input.txt").read_text().splitlines()
    return [int(lines[0].split(": ")[1]), int(lines[1].split(": ")[1])]


def move(number: int) -> int:

    return 10 if number % 10 == 0 else number % 10


def deterministic_dice(positions: list[int]) -> int:
    def dice() -> Iterator[int]:
        value = 0
        while True:
            value += 1
            if value == 101:
                value = 1
            yield value

    scores = [0, 0]
    roll = dice()
    dice_rolls = 0
    positions = positions[:]

    while all(score < 1000 for score in scores):
        for player in (0, 1):
            dice_sum = next(roll) + next(roll) + next(roll)
            dice_rolls += 3
            space = move(positions[player] + dice_sum)
            positions[player] = space
            scores[player] += space
            if scores[player] >= 1000:
                break

    return min(scores) * dice_rolls


def dirac_dice(positions: list[int]) -> tuple[int, int]:

    rolls = [
        (3, 1),
        (4, 3),
        (5, 6),
        (6, 7),
        (7, 6),
        (8, 3),
        (9, 1),
    ]

    @functools.cache
    def play(scores: tuple[int, int], positions: tuple[int, int]) -> tuple[int, int]:

        if any(score >= 21 for score in scores):
            return (1, 0) if scores[0] >= 21 else (0, 1)

        wins = (0, 0)
        for roll_1, roll_1_count in rolls:
            p1_pos = move(positions[0] + roll_1)

            if scores[0] + p1_pos >= 21:
                wins = (wins[0] + roll_1_count, wins[1])
                continue

            for _ in range(roll_1_count):
                for roll_2, roll_2_count in rolls:
                    p2_pos = move(positions[1] + roll_2)
                    for _ in range(roll_2_count):
                        p1, p2 = play(
                            (scores[0] + p1_pos, scores[1] + p2_pos),
                            (p1_pos, p2_pos),
                        )
                        wins = (wins[0] + p1, wins[1] + p2)
        return wins

    return play((0, 0), (positions[0], positions[1]))


def solve() -> None:

    positions = parse_input()

    # First part
    assert deterministic_dice(positions) == 752745

    # Second part
    assert max(dirac_dice(positions)) == 309196008717909


if __name__ == "__main__":
    solve()
