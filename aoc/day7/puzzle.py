import sys
from typing import Callable
from collections import Counter
from pathlib import Path


def parse_input() -> list[int]:
    return [
        int(value)
        for value in (Path(__file__).parent / "input.txt").read_text().split(",")
    ]


def minimum_cost(crabs: dict[int, int], cost: Callable[[int], int]) -> int:

    cheapest = sys.maxsize
    for position in range(max(crabs.keys())):
        fuel = 0
        for crab, count in crabs.items():
            fuel += cost(abs(crab - position)) * count
            if fuel >= cheapest:
                break
        cheapest = min(cheapest, fuel)
    return cheapest


def solve() -> None:

    positions = parse_input()

    crabs = Counter(positions)

    # First part
    def constant_cost(n: int) -> int:
        return n

    assert minimum_cost(crabs, constant_cost) == 344138

    # Second part
    def nonconstant_cost(n: int) -> int:
        return (n ** 2 + n) // 2

    assert minimum_cost(crabs, nonconstant_cost) == 94862124


if __name__ == "__main__":
    solve()
