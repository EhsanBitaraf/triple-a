import click
from triplea.service.repository.pipeline_flag import (
    go_article_review_by_llm,
    go_extract_triple,
    go_affiliation_mining,
    go_extract_topic,
    go_article_embedding,
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
    elif name == "FlagEmbedding":
        go_article_embedding()
    elif name == "FlagShortReviewByLLM":
        go_article_review_by_llm()

    else:
        raise NotImplementedError
