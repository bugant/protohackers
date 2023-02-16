import asyncio
import logging

from proto_means_to_an_end import api, packet


MEANS_PORT = 8001
BACKLOG_CONNECTIONS = 10
MAX_WORKER = 10


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run_server(port: int):
    asyncio.run(start_server(port))


async def start_server(port: int):
    server = await asyncio.start_server(handle_session, "", port)
    logger.info("means-to-an-end listening on port %s", port)
    async with server:
        await server.serve_forever()


async def handle_session(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    logger.info("starting session")
    session = api.new_session()
    msg = b""
    while True:
        logger.debug("reading message")
        data = await reader.read(packet.PACKET_SIZE)
        if data == b"":
            break
        msg += data
        logger.debug("data=%s, msg=%s (%s)", data, msg, len(msg))
        if len(msg) >= packet.PACKET_SIZE:
            pack_ = msg[:packet.PACKET_SIZE]
            msg = msg[packet.PACKET_SIZE:]
            logger.debug("got message: %s", pack_)
            resp = api.process_packet(pack_, session)
            if resp is not None:
                writer.write(resp)
                await writer.drain()
    writer.close()
    logger.info("closing session")
