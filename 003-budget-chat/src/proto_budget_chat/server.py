import asyncio
import functools
import logging
import uuid

from . import chat


CHAT_PORT = 8001
BACKLOG_CONNECTIONS = 10


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def run_server(port: int):
    asyncio.run(start_server(port))


async def start_server(port: int):
    chat_server = asyncio.Queue()
    user_session_cb = functools.partial(user_session, chat_server)
    server = await asyncio.start_server(user_session_cb, "", port)
    logger.info("budget-chat listening on port %s", port)
    async with asyncio.TaskGroup() as server_tasks:
        server_tasks.create_task(server.serve_forever())
        server_tasks.create_task(chat.chat_server(chat_server))


async def user_session(
    chat_server: asyncio.Queue,
    reader: asyncio.StreamReader,
    writer: asyncio.StreamWriter
) -> None:
    logger.info("starting new user session")
    writer.write("please identify yourself\n".encode("ascii"))
    await writer.drain()

    username = await reader.readline()
    username = username.decode("ascii").strip()
    logger.debug("got username %s", username)
    if username:
        u_queue = asyncio.Queue()
        user = chat.User(uuid=uuid.uuid4(), queue=u_queue, username=username, writer=writer)
        await chat_server.put(chat.ChatMessage(user=user, type=chat.MsgType.JOIN))

        async with asyncio.TaskGroup() as tasks:
            tasks.create_task(chat.chat_user(user, writer))
            tasks.create_task(chat.user_input(user, reader, chat_server))

    writer.close()
    await writer.wait_closed()
    logger.info("closing session")
