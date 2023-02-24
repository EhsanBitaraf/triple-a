import click
from triplea.service.click_logger import logger
from triplea import __version__

@click.command()
# @click.argument('cli')
# @click.option("--command", "-c" , "command",  prompt='Your name please',  required=False , help="Add a thematic break")
@click.option("--action", "-a" , "action", required=False , is_flag=True, show_default=True, default=True, help="Add a thematic break")
@click.option("--version", "-v" , "version", required=False , is_flag=True, help="output version information and exit")
def main(action,version):
    if version:
        logger.INFO(__version__)

    



if __name__ == '__main__':
    main()