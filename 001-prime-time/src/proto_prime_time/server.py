import json
import logging
import signal
import socket
import sys
from multiprocessing import Pool

import attr

from proto_prime_time import api

PRIME_PORT = 8001
BACKLOG_CONNECTIONS = 10
READ_CHUNK_SIZE = 1
MAX_WORKER = 10
LINE_DELIMITER = ord("\n")


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run_server(port: int) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", port))
    sock.listen(BACKLOG_CONNECTIONS)
    logger.info("prime server listening on port %s", port)

    with Pool(processes=MAX_WORKER) as pool:
        signal.signal(signal.SIGINT, shutdown(sock, pool))

        while True:
            conn, addr = sock.accept()
            pool.apply_async(handle_session, (conn, addr))


def handle_session(conn: socket.SocketIO, addr) -> None:
    logging.info(f"started new prime session {addr}")
    msg = b""
    with conn:
        while True:
            try:
                logger.debug("reading data from %s", addr)
                data = conn.recv(READ_CHUNK_SIZE, socket.MSG_DONTWAIT)
                if data == b"":
                    break
                logger.debug("got data from %s: %s", addr, data)
                msg += data
                if data[-1] != LINE_DELIMITER:
                    continue

                handle_req(conn, msg)
                msg = b""
            except BlockingIOError as err:
                logger.debug("no data ready for read: %s", err)
                pass
        conn.shutdown(socket.SHUT_RDWR)
    logger.info("closing session %s", addr)


def handle_req(conn: socket.SocketIO, msg: bytes) -> None:
    logger.info("processing request %s", msg)
    resp = None
    try:
        resp = api.process_request(json.loads(msg))
    except Exception:
        logger.exception("invalid msg: %s", msg)
    logger.info("got resp: %s", resp)
    if resp is None:
        conn.sendall((json.dumps({}) + "\n").encode())
    else:
        conn.sendall((json.dumps(attr.asdict(resp)) + "\n").encode())


def shutdown(sock: socket.SocketIO, pool: Pool) -> callable:
    def _shutdown(_signum, _frame):
        logger.info("shutting down...")
        pool.terminate()
        pool.join()
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        sys.exit(0)

    return _shutdown


if __name__ == "__main__":
    run_server()
