import click
from triplea import __version__


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"version  {__version__}")
    ctx.exit()


@click.group()
@click.option(
    "--version",
    "-v",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
)
def cli():
    pass
    # click.echo(f"Debug mode is {'on' if debug else 'off'}")
