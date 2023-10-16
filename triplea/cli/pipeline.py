import click
from triplea.service.repository.pipeline_flag import (
    go_extract_triple,
    go_affiliation_mining,
    go_extract_topic,
)
from triplea.cli.main import cli


@cli.command("pipeline", help="Run Custom PipeLine in arepo.")
@click.option("--name", "-n", "name", help="Name of pipeline")
def pipeline(name: str):
    if name == "FlagExtractKG":
        go_extract_triple()
    elif name == "FlagExtractTopic":
        go_extract_topic()
    elif name == "FlagAffiliationMining":
        go_affiliation_mining()
    elif name == "FlagAffiliationMining_Titipata":
        go_affiliation_mining(method="Titipata")

    else:
        raise NotImplementedError
