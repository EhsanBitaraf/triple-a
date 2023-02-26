import click
import triplea as tr

click.echo(f"Title: {tr.__title__} ({tr.__version__})")
click.echo(f"   {tr.__description__}")
click.echo()

from triplea.cli.main import cli             # main.py
from triplea.cli.import_bib import import_single_file # import
from triplea.cli.config import configuration # config
from triplea.cli.ner import ner_title        # ner
from triplea.cli.next import next            # next
from triplea.cli.search import get_article   # search
from triplea.cli.go import go                # go
from triplea.cli.export import export        # export
from triplea.cli.visualize import visualize  # visualize
from triplea.cli.analysis import analysis    # analysis
from triplea.cli.arepo import arepo          # arepo

if __name__ == '__main__':
    cli()