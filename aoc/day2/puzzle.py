from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Command:
    direction: str
    units: int


def parse_input() -> list[Command]:

    commands = []
    for line in (Path(__file__).parent / "input.txt").read_text().splitlines():
        direction, unit = line.split()
        commands.append(Command(direction, int(unit)))
    return commands


def navigate(commands: list[Command], use_aim: bool = False) -> int:

    x = 0
    y = 0
    aim = 0
    for command in commands:
        match command:
            case Command("forward", units) if use_aim:
                x += units
                y += aim * units
            case Command("forward", units):
                x += units
            case Command("up", units) if use_aim:
                aim -= units
            case Command("up", units):
                y -= units
            case Command("down", units) if use_aim:
                aim += units
            case Command("down", units):
                y += units
    return x * y


def solve() -> None:

    commands = parse_input()

    # First part
    assert navigate(commands) == 1636725

    # Second part
    assert navigate(commands, use_aim=True) == 1872757425


if __name__ == "__main__":
    solve()
