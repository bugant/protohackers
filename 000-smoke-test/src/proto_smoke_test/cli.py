import logging

import click

from proto_smoke_test import echo


logging.basicConfig(level=logging.INFO)


@click.group()
def cli():
    pass


@cli.command()
def echo_server():
    click.secho(f"starting echo server on port {echo.ECHO_PORT}")
    echo.run_server(echo.ECHO_PORT)
