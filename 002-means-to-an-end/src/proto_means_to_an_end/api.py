from collections import deque
import logging
import typing

from proto_means_to_an_end import packet, price


logger = logging.getLogger()


def new_session() -> typing.Deque[price.Price]:
    return deque()


def process_packet(pack: bytes, session: typing.Deque[price.Price]) -> typing.Optional[bytes]:
    req = packet.from_bytes(pack)
    logger.info("processing %s", req)
    if req.packet_type == packet.PacketType.INSERT:
        session.append(price.Price(
            timestamp=req.param_1,
            price=req.param_2,
        ))
        return None
    else:
        avg = price.avg(session, req.param_1, req.param_2)
        logger.info("avg=%s", avg)
        return avg.to_bytes(4, byteorder="big", signed=True)
