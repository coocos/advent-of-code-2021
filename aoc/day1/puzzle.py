from pathlib import Path


def parse_input() -> list[int]:
    return [
        int(depth)
        for depth in (Path(__file__).parent / "input.txt").read_text().splitlines()
    ]


def count_increases(values: list[int]) -> int:
    return sum(int(second - first > 0) for first, second in zip(values, values[1:]))


def solve() -> None:

    measurements = parse_input()

    # First part
    assert count_increases(measurements) == 1374

    # Second part
    windows = [sum(measurements[x : x + 3]) for x in range(len(measurements) - 2)]
    assert count_increases(windows) == 1418


if __name__ == "__main__":
    solve()
