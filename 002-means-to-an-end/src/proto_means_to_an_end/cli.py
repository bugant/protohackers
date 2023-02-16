import logging

import click


from proto_means_to_an_end import server


logging.basicConfig(level=logging.INFO)


@click.group()
def cli():
    pass


@cli.command()
def avg_server():
    server.run_server(server.MEANS_PORT)
