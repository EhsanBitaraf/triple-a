import click
import triplea as tr
from triplea.cli.main import cli  # main.py
from triplea.cli.import_bib import import_single_file  # importbib # noqa: F401
from triplea.cli.import_file import import_file  # import # noqa: F401
from triplea.cli.config import configuration  # config # noqa: F401
from triplea.cli.ner import ner_title  # ner # noqa: F401
from triplea.cli.next import next  # next # noqa: F401
from triplea.cli.search import get_article  # search # noqa: F401
from triplea.cli.go import go  # go # noqa: F401
from triplea.cli.export_graph import export_graph  # exportgraph # noqa: F401
from triplea.cli.export import export  # export # noqa: F401
from triplea.cli.export_pretrain_llm import export_llm  # exportllm # noqa: F401
from triplea.cli.export_article import cli_export_article  # export_article # noqa: F401
from triplea.cli.visualize import visualize  # visualize # noqa: F401
from triplea.cli.visualize import visualize_file  # visualize_file # noqa: F401
from triplea.cli.analysis import analysis  # analysis # noqa: F401
from triplea.cli.arepo import arepo  # arepo # noqa: F401
from triplea.cli.pipeline import pipeline  # pipeline # noqa: F401

click.echo(f"Title: {tr.__title__} ({tr.__version__})")
click.echo(f"   {tr.__description__}")
click.echo()

if __name__ == "__main__":
    cli()
