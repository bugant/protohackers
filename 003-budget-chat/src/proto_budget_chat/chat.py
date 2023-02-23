import asyncio
from collections import deque
import enum
import logging
import re
import uuid

import attrs


logger = logging.getLogger()


@attrs.define
class User:
    uuid: uuid.UUID
    username: str
    queue: asyncio.Queue
    writer: asyncio.StreamWriter


class MsgType(enum.Enum):
    JOIN = "join"
    LEAVE = "leave"
    PRESENCE = "presence"
    USER_JOINED = "joined"
    CHAT = "chat"
    QUIT = "quit"


@attrs.define
class ChatMessage:
    user: User
    type: MsgType
    msg: None | str = attrs.field(default=None)


async def chat_server(queue):
    online_users: deque[str] = []
    users: dict[str, User] = {}
    while True:
        msg = await queue.get()
        logger.debug("chat server got %s", msg)
        if msg.type is MsgType.JOIN:
            new_user = msg.user
            if not valid_username(new_user):
                await quit_user(new_user)
            if new_user.username not in online_users:
                online_users.append(new_user.username)
                users[new_user.uuid] = new_user
                for _, user in users.items():
                    await notify_presence(user, new_user, users)
            else:
                await quit_user(new_user)
        elif msg.type is MsgType.LEAVE:
            if msg.user.uuid in users:
                online_users.remove(msg.user.username)
                del users[msg.user.uuid]
                await notify_quit(msg.user)
                for _, user in users.items():
                    await notify_leave(user, msg.user)
        elif msg.type is MsgType.CHAT:
            for _, user in users.items():
                await notify_chat(user, msg.user, msg.msg)
        queue.task_done()


async def chat_user(u: User, writer: asyncio.StreamWriter) -> None:
    while True:
        msg = await u.queue.get()
        quitting = False
        to_send: None | str = None
        logger.debug("chat user got %s", msg)
        if msg.type is MsgType.PRESENCE:
            to_send = f"* The room contains: {msg.msg}\n"
        elif msg.type is MsgType.USER_JOINED:
            to_send = f"* {msg.msg} has entered the room\n"
        elif msg.type is MsgType.CHAT:
            to_send = f"{msg.msg}\n"
        elif msg.type is MsgType.LEAVE:
            to_send = f"* {msg.msg} has left the room\n"
        elif msg.type is MsgType.QUIT:
            quitting = True

        if to_send:
            writer.write(to_send.encode("ascii"))
            await writer.drain()
        u.queue.task_done()
        if quitting:
            if not u.writer.is_closing():
                u.writer.close()
                await u.writer.wait_closed()
            break


async def user_input(u: User, reader: asyncio.StreamReader, chat_server: asyncio.Queue) -> None:
    while True:
        msg = await reader.readline()
        if not msg:
            await chat_server.put(ChatMessage(u, type=MsgType.LEAVE))
            break
        msg = msg.decode("ascii").strip()
        logger.debug("got %s from %s", msg, u)
        await chat_server.put(ChatMessage(u, type=MsgType.CHAT, msg=msg))


async def notify_presence(u: User, new_user: User, users: dict[str, User]) -> None:
    if u.uuid == new_user.uuid:
        await u.queue.put(
            ChatMessage(user=u, type=MsgType.PRESENCE, msg=", ".join(u.username for u in users.values() if u != new_user))
        )
    else:
        await u.queue.put(
            ChatMessage(user=u, type=MsgType.USER_JOINED, msg=new_user.username)
        )


async def notify_chat(u: User, sender: User, msg: str) -> None:
    if u.uuid == sender.uuid:
        return

    await u.queue.put(ChatMessage(user=u, type=MsgType.CHAT, msg=f"[{sender.username}] {msg}"))


async def notify_leave(u: User, gone: User) -> None:
    await u.queue.put(ChatMessage(user=u, type=MsgType.LEAVE, msg=gone.username))


async def notify_quit(u: User) -> None:
    await u.queue.put(ChatMessage(user=u, type=MsgType.QUIT))


def valid_username(u: User) -> bool:
    return re.match(r"^[a-zA-Z0-9]+$", u.username) is not None


async def quit_user(u: User) -> None:
    await u.queue.put(ChatMessage(user=u, type=MsgType.QUIT))
