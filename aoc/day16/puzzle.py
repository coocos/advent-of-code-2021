import operator
from functools import reduce
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Packet:

    version: int
    type: int
    value: int = 0
    length: int = 0

    packets: list["Packet"] = field(default_factory=list)


def parse_input() -> str:

    packet = (Path(__file__).parent / "input.txt").read_text()
    return bin(int(packet, 16))[2:].zfill(len(packet) * 4)


def decode(packet: str) -> Packet:

    version = int(packet[:3], 2)
    type = int(packet[3:6], 2)

    if type == 4:
        payload = packet[6:]
        length = 6
        number = ""
        while payload:
            more = payload[0]
            number += payload[1:5]
            length += 5
            if not int(more):
                break
            payload = payload[5:]
        number = int(number, 2)
        return Packet(version, type, number, length)
    else:
        mode = int(packet[6])
        if mode:
            sub_packet_count = int(packet[7 : 7 + 11], 2)
            sub_packet_bits = packet[7 + 11 :]
            sub_packets = []
            while len(sub_packets) < sub_packet_count:
                sub_packet = decode(sub_packet_bits)
                sub_packet_bits = sub_packet_bits[sub_packet.length :]
                sub_packets.append(sub_packet)
            return Packet(
                version,
                type,
                0,
                6 + 11 + sum(packet.length for packet in sub_packets) + 1,
                sub_packets,
            )
        else:
            sub_packets = []
            sub_packet_size = int(packet[7 : 7 + 15], 2)
            sub_packet_bits = packet[7 + 15 :]
            while (
                sum(sub_packet.length for sub_packet in sub_packets) < sub_packet_size
            ):
                sub_packet = decode(sub_packet_bits)
                sub_packets.append(sub_packet)
                sub_packet_bits = sub_packet_bits[sub_packet.length :]
            return Packet(
                version,
                type,
                0,
                6 + 15 + sub_packet_size + 1,
                sub_packets,
            )


def version_sum(packet: Packet, depth: int = 0) -> int:

    if not packet.packets:
        return packet.version

    versions = packet.version
    for sub_packet in packet.packets:
        versions += version_sum(sub_packet, depth + 1)
    return versions


def visit(packet: Packet) -> int:

    if packet.type == 0:
        return sum(visit(p) for p in packet.packets)
    elif packet.type == 1:
        return reduce(operator.mul, (visit(p) for p in packet.packets))
    elif packet.type == 2:
        return min(visit(p) for p in packet.packets)
    elif packet.type == 3:
        return max(visit(p) for p in packet.packets)
    elif packet.type == 4:
        return packet.value
    elif packet.type == 5:
        first, second = packet.packets
        return int(visit(first) > visit(second))
    elif packet.type == 6:
        first, second = packet.packets
        return int(visit(first) < visit(second))
    else:
        first, second = packet.packets
        return int(visit(first) == visit(second))


def solve() -> None:

    packet = parse_input()

    # First part
    assert version_sum(decode(packet)) == 940

    # Second part
    assert visit(decode(packet)) == 13476220616073


if __name__ == "__main__":
    solve()
