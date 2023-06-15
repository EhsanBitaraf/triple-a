import click
from triplea.service.repository.pipeline_flag import go_extract_triple
from triplea.cli.main import cli


@cli.command("pipeline", help="Run Custom PipeLine in arepo.")
@click.option("--name", "-n","name", help="Name of pipeline")
def pipeline(name: str):
    if name == "FlagExtractKG":
        go_extract_triple()
    elif name == "FlagExtractTopic":
        pass
    else:
        raise NotImplementedError
