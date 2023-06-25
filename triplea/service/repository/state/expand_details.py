import sys
import time
from triplea.client.pubmed import get_article_details_from_pubmed
from triplea.config.settings import SETTINGS
from triplea.schemas.article import Article
from triplea.service.click_logger import logger

tps_limit = SETTINGS.AAA_TPS_LIMIT


def expand_details(article: Article) -> Article:
    article.State = 1
    sleep_time = 1 / tps_limit
    time.sleep(sleep_time)
    try:
        oa = get_article_details_from_pubmed(article.PMID)
        article.OreginalArticle = oa
    except Exception:
        article.State = 0
        exc_type, exc_value, exc_tb = sys.exc_info()
        print()
        logger.ERROR(f"Error {exc_type} Value : {exc_value}")
        logger.ERROR(f"Error {exc_tb}")

    return article
