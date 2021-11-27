from pathlib import Path


def parse_input() -> str:
    return (Path(__file__).parent / "input.txt").read_text()


def solve() -> None:
    print(parse_input())


if __name__ == "__main__":
    solve()
