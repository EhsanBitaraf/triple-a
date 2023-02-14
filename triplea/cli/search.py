import click
from triplea.service.repository.state import get_article_list_from_pubmed_all_store_to_arepo
from triplea.service.click_logger import logger

@click.command()
@click.option("--searchterm", prompt="Search Term", help="Query for Pubmed search.")
def get_article(searchterm):
    logger.INFO(f'Searching Pubmed ...')
    # searchterm = searchterm.replace(' ', '+')
    searchterm = searchterm.strip()
    logger.INFO(f'Query encoder : ')
    logger.INFO(searchterm, forecolore='cyan')
    get_article_list_from_pubmed_all_store_to_arepo(searchterm)

if __name__ == '__main__':
    pass
    get_article()