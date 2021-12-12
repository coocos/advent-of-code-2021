from collections import defaultdict
from pathlib import Path


Graph = dict[str, list[str]]


def parse_input() -> Graph:
    graph: Graph = defaultdict(list)
    for line in (Path(__file__).parent / "input.txt").read_text().splitlines():
        start, end = line.split("-")
        graph[start].append(end)
        graph[end].append(start)
    return graph


def paths(caves: Graph, path: list[str], visited: set[str]) -> int:

    if path[-1] == "end":
        return 1

    path_count = 0
    for cave in caves[path[-1]]:
        if cave.islower() and cave in visited:
            continue
        path_count += paths(caves, path + [cave], visited | {cave})

    return path_count


def paths_using_cave_twice(
    caves: Graph, path: list[str], visited: set[str], twice: str = ""
) -> int:

    if path[-1] == "end":
        return 1

    path_count = 0
    for cave in caves[path[-1]]:
        if cave == "start":
            continue
        elif cave.islower() and cave in visited:
            if not twice:
                path_count += paths_using_cave_twice(
                    caves, path + [cave], visited | {cave}, cave
                )
        else:
            path_count += paths_using_cave_twice(
                caves, path + [cave], visited | {cave}, twice
            )
    return path_count


def solve() -> None:
    caves = parse_input()

    # First part
    assert paths(caves, ["start"], {"start"}) == 3410

    # Second part
    assert paths_using_cave_twice(caves, ["start"], {"start"}) == 98796


if __name__ == "__main__":
    solve()
