from itertools import pairwise
from collections import defaultdict, Counter
from pathlib import Path


def parse_input() -> tuple[str, dict[str, str]]:

    lines = (Path(__file__).parent / "input.txt").read_text().splitlines()
    return lines[0], dict(rule.split(" -> ") for rule in lines[2:])


def insert_pairs(
    pairs: dict[str, int], rules: dict[str, str], elements: dict[str, int], step: int
) -> int:

    if step == 0:
        return max(elements.values()) - min(elements.values())

    next_gen_pairs = defaultdict(int)
    for (a, b), count in pairs.items():
        element = rules[a + b]
        next_gen_pairs[a + element] += count
        next_gen_pairs[element + b] += count
        elements[element] += count

    return insert_pairs(next_gen_pairs, rules, elements, step - 1)


def solve() -> None:

    template, rules = parse_input()

    pairs = Counter(a + b for a, b in pairwise(template))
    elements = Counter(template)

    # First part
    assert insert_pairs(pairs, rules, elements.copy(), 10) == 3411

    # Second part
    assert insert_pairs(pairs, rules, elements.copy(), 40) == 7477815755570


if __name__ == "__main__":
    solve()
