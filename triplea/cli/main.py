import click

# @click.command()
# @click.option("--count", default=1, help="Number of greetings.")
# @click.option("--name", prompt="Your name", help="The person to greet.")
# def hello(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for _ in range(count):
#         click.echo(f"Hello, {name}!")


# @cli.command()
# # @click.argument('cli')
# # @click.option("--command", "-c" , "command",  prompt='Your name please',  required=False , help="Add a thematic break")
# @cli.option("--action", "-a" , "action", required=False , is_flag=True, show_default=True, default=True, help="Add a thematic break")
# @cli.option("--version", "-v" , "version", required=False , is_flag=True, help="output version information and exit")
# def main(action,version):
#     if version:
#         logger.INFO(__version__)


@click.group()
def cli():
    pass
    # click.echo(f"Debug mode is {'on' if debug else 'off'}")
