import logging

import click

from proto_prime_time import server

logging.basicConfig(level=logging.INFO)


@click.group()
def cli():
    pass


@cli.command()
def prime_server():
    server.run_server(8001)
