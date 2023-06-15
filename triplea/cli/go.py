import click
from triplea.service.repository.pipeline_core import move_state_until
from triplea.cli.main import cli


@cli.command("go", help="Moves the articles state in the Arepo until end state.")
@click.option("--end", "-e", "end_state", help="last state")
def go(end_state: int):
    move_state_until(end_state)
