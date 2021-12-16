from __future__ import annotations
import operator
from functools import reduce
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LiteralPacket:

    version: int
    type: int
    value: int
    size: int


@dataclass
class OperatorPacket:

    version: int
    type: int
    mode: int

    packets: list[OperatorPacket | LiteralPacket] = field(default_factory=list)

    @property
    def size(self) -> int:
        return sum(p.size for p in self.packets) + (18 if self.mode else 22)


def parse_input() -> str:

    packet = (Path(__file__).parent / "input.txt").read_text()
    return bin(int(packet, 16))[2:].zfill(len(packet) * 4)


def decode(bits: str) -> LiteralPacket | OperatorPacket:

    version = int(bits[:3], 2)
    type = int(bits[3:6], 2)

    payload = bits[6:]

    if type == 4:
        size = 6
        number = ""
        while payload:
            more = int(payload[0])
            number += payload[1:5]
            size += 5
            if not more:
                break
            payload = payload[5:]
        return LiteralPacket(version, type, int(number, 2), size)
    else:
        mode = int(payload[0])
        sub_packets = []
        if mode:
            sub_packet_count = int(payload[1:12], 2)
            sub_packet_bits = payload[12:]
            while len(sub_packets) < sub_packet_count:
                sub_packets.append(decode(sub_packet_bits))
                sub_packet_bits = sub_packet_bits[sub_packets[-1].size :]
        else:
            sub_packet_size = int(payload[1:16], 2)
            sub_packet_bits = payload[16:]
            while sum(p.size for p in sub_packets) < sub_packet_size:
                sub_packets.append(decode(sub_packet_bits))
                sub_packet_bits = sub_packet_bits[sub_packets[-1].size :]
        return OperatorPacket(
            version,
            type,
            mode,
            sub_packets,
        )


def version_sum(packet: LiteralPacket | OperatorPacket) -> int:

    if isinstance(packet, LiteralPacket):
        return packet.version

    return packet.version + sum(version_sum(p) for p in packet.packets)


def visit(packet: LiteralPacket | OperatorPacket) -> int:

    if isinstance(packet, LiteralPacket):
        return packet.value

    return {
        0: lambda packet: sum(visit(p) for p in packet.packets),
        1: lambda packet: reduce(operator.mul, (visit(p) for p in packet.packets)),
        2: lambda packet: min(visit(p) for p in packet.packets),
        3: lambda packet: max(visit(p) for p in packet.packets),
        5: lambda packet: int(visit(packet.packets[0]) > visit(packet.packets[1])),
        6: lambda packet: int(visit(packet.packets[0]) < visit(packet.packets[1])),
        7: lambda packet: int(visit(packet.packets[0]) == visit(packet.packets[1])),
    }[packet.type](packet)


def solve() -> None:

    packet = parse_input()

    # First part
    assert version_sum(decode(packet)) == 940

    # Second part
    assert visit(decode(packet)) == 13476220616073


if __name__ == "__main__":
    solve()
