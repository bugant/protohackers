import pytest

from proto_means_to_an_end import packet


@pytest.mark.parametrize("payload,packtype,p1,p2", (
    (b"\x49\x00\x00\x30\x39\x00\x00\x00\x65", packet.PacketType.INSERT, 12345, 101),
    (b"\x49\x00\x00\x30\x3a\x00\x00\x00\x66", packet.PacketType.INSERT, 12346, 102),
    (b"\x49\x00\x00\x30\x3b\x00\x00\x00\x64", packet.PacketType.INSERT, 12347, 100),
    (b"\x49\x00\x00\xa0\x00\x00\x00\x00\x05", packet.PacketType.INSERT, 40960, 5),
    (b"\x51\x00\x00\x30\x00\x00\x00\x40\x00", packet.PacketType.QUERY, 12288, 16384),
))
def test_from_bytes(payload, packtype, p1, p2):
    pack = packet.from_bytes(payload)
    assert packtype == pack.packet_type
    assert p1 == pack.param_1
    assert p2 == pack.param_2
