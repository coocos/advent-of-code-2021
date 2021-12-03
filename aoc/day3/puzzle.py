import operator
from pathlib import Path
from typing import Callable


def parse_input() -> list[int]:
    return [
        int(line, 2)
        for line in (Path(__file__).parent / "input.txt").read_text().splitlines()
    ]


def power_consumption(values: list[int]) -> int:

    bits = max(values).bit_length()

    ones = [0] * bits
    for value in values:
        for bit in range(bits):
            ones[bit] += value >> bit & 1

    gamma = 0
    for count in reversed(ones):
        if count > len(values) / 2:
            gamma |= 1
        gamma <<= 1
    gamma >>= 1

    epsilon = gamma ^ 0xFFF
    return gamma * epsilon


def life_support_rating(values: list[int]) -> int:
    def find(values: list[int], compare: Callable[[int, int], bool]) -> int:
        bits = max(values).bit_length() - 1
        while len(values) > 1:
            ones = [value for value in values if value >> bits & 1]
            zeroes = [value for value in values if not value >> bits & 1]
            values = ones if compare(len(ones), len(zeroes)) else zeroes
            bits -= 1
        return values.pop()

    oxygen = find(values, operator.ge)
    scrubber = find(values, operator.lt)

    return scrubber * oxygen


def solve() -> None:

    values = parse_input()

    # First part
    assert power_consumption(values) == 4006064

    # Second part
    assert life_support_rating(values) == 5941884


if __name__ == "__main__":
    solve()
