import enum

import attrs


PACKET_SIZE = 9


class PacketType(enum.Enum):
    QUERY = ord("Q")
    INSERT = ord("I")


def _int_from_bytes(val: bytes | int) -> int:
    if isinstance(val, bytes):
        return int.from_bytes(val, byteorder="big", signed=True)
    else:
        return val


def _to_packet_type(val: int | PacketType) -> PacketType:
    if isinstance(val, int):
        return PacketType(val)
    return val


@attrs.define
class Packet:
    packet_type: PacketType = attrs.field(validator=attrs.validators.in_(PacketType), converter=_to_packet_type)
    param_1: int = attrs.field(converter=_int_from_bytes, validator=attrs.validators.instance_of(int))
    param_2: int = attrs.field(converter=_int_from_bytes, validator=attrs.validators.instance_of(int))


def from_bytes(payload: bytes) -> Packet:
    if len(payload) != PACKET_SIZE:
        raise ValueError("Packet must be 9 bytes long")
    return Packet(
        packet_type=payload[0],
        param_1=payload[1:5],
        param_2=payload[5:],
    )
