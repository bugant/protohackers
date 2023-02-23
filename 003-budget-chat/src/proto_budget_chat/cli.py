import logging

import click

from proto_budget_chat import server


logging.basicConfig(level=logging.INFO)


@click.group
def cli():
    pass


@cli.command
def chat_server():
    server.run_server(server.CHAT_PORT)
