import click
from triplea.service.general import get_article_list_all_store_to_kg_rep
from triplea.service.click_logger import logger

@click.command()
@click.option("--searchterm", prompt="Search Term", help="Query for Pubmed search.")
def get_article(searchterm):
    logger.INFO(f'Searching Pubmed ...')
    # searchterm = searchterm.replace(' ', '+')
    searchterm = searchterm.strip()
    logger.INFO(f'Query encoder : ')
    logger.INFO(searchterm, forecolore='cyan')
    get_article_list_all_store_to_kg_rep(searchterm)

if __name__ == '__main__':
    pass
    get_article()