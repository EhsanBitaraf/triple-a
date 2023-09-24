import click
from triplea.service.repository.state import (
    get_article_list_from_pubmed_all_store_to_arepo,
)
from triplea.service.click_logger import logger
from triplea.cli.main import cli


@cli.command("search", help="Search query from PubMed and store to Arepo.")
@click.option(
    "--searchterm",
    "-s",
    "searchterm",
    prompt="Search Term",
    help="Query for Pubmed search.",
)
def get_article(searchterm):
    logger.DEBUG(f"searchterm : {searchterm}")
    logger.INFO("Searching Pubmed ...")

    # searchterm = searchterm.replace(' ', '+')
    searchterm = searchterm.strip()
    logger.INFO("Query encoder : ")
    logger.INFO(searchterm, forecolore="cyan")
    get_article_list_from_pubmed_all_store_to_arepo(searchterm)


if __name__ == "__main__":
    pass
    get_article()
