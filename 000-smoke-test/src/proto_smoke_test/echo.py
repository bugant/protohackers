import logging
from multiprocessing import Pool
import signal
import socket
import sys

ECHO_PORT = 8001
BACKLOG_CONNECTIONS = 10
READ_CHUNK_SIZE = 1024
MAX_WORKER = 10


logger = logging.getLogger(__name__)


def handle_echo(conn: socket.SocketIO, addr) -> None:
    logging.info(f"got new connection from {addr}")
    with conn:
        while True:
            try:
                logger.debug("reading data from %s", addr)
                data = conn.recv(READ_CHUNK_SIZE, socket.MSG_DONTWAIT)
                logger.debug("got data from %s: %s", addr, data)
                conn.sendall(data)
                if len(data) == 0:
                    break
            except BlockingIOError:
                break
        conn.shutdown(socket.SHUT_RDWR)
    logger.info("done serving %s", addr)


def shutdown(sock: socket.SocketIO, pool: Pool) -> callable:
    def _shutdown(_signum, _frame):
        logger.info("shutting down...")
        pool.terminate()
        pool.join()
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
        sys.exit(0)

    return _shutdown


def run_server(port: int) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("", port))
    sock.listen(BACKLOG_CONNECTIONS)

    with Pool(processes=MAX_WORKER) as pool:
        signal.signal(signal.SIGINT, shutdown(sock, pool))

        while True:
            conn, addr = sock.accept()
            pool.apply_async(handle_echo, (conn, addr))


if __name__ == "__main__":
    run_server()
