from typing import Iterable
from pathlib import Path

VALID_DIGITS = {
    "abcefg": "0",
    "cf": "1",
    "acdeg": "2",
    "acdfg": "3",
    "bcdf": "4",
    "abdfg": "5",
    "abdefg": "6",
    "acf": "7",
    "abcdefg": "8",
    "abcdfg": "9",
}


def parse_input() -> list[tuple[str, str]]:
    entries = []
    for line in (Path(__file__).parent / "input.txt").read_text().splitlines():
        signals, digits = line.split(" | ")
        entries.append((signals.split(), digits.split()))
    return entries


def signal_to_digit(signal: Iterable[str], wire_map: dict[str, str]) -> str:
    return "".join(sorted(wire_map[s] for s in signal))


def possible_wirings(
    wires: set[str], segments: set[str], wiring_map: dict[str, str]
) -> Iterable[dict[str, str]]:
    if not wires:
        yield wiring_map

    for wire in wires:
        for segment in segments:
            yield from possible_wirings(
                wires - {wire},
                segments - {segment},
                wiring_map | {wire: segment},
            )


def find_correct_wiring(
    unknown_signals: list[set[str]],
    remaining_segments: set[str],
    wiring_map: dict[str, str],
) -> dict[str, str]:

    if not unknown_signals:
        return wiring_map

    signal = unknown_signals[-1]
    unknown_wires = {wire for wire in signal if wire not in wiring_map}

    for map in possible_wirings(unknown_wires, remaining_segments, wiring_map):
        if signal_to_digit(signal, map) in VALID_DIGITS:
            if wiring_map := find_correct_wiring(
                unknown_signals[:-1], remaining_segments - set(map.values()), map
            ):
                return wiring_map
    return {}


def solve() -> None:

    entries = parse_input()

    # First part
    count = 0
    for signals, digits in entries:
        for digit in digits:
            if len(digit) in (2, 4, 3, 7):
                count += 1

    assert count == 532

    # Second part
    output_sum = 0
    for signals, digits in entries:
        signals = sorted([set(s) for s in signals], key=lambda s: len(s), reverse=True)
        wiring_map = find_correct_wiring(signals, set("abcdefg"), {})
        display = [VALID_DIGITS[signal_to_digit(digit, wiring_map)] for digit in digits]
        output_sum += int("".join(display))

    assert output_sum == 1011284


if __name__ == "__main__":
    solve()
