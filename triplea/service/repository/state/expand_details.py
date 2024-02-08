import time
from triplea.client.pubmed import get_article_details_from_pubmed
from triplea.config.settings import SETTINGS
from triplea.schemas.article import Article, SourceBankType
from triplea.utils.general import print_error

tps_limit = SETTINGS.AAA_TPS_LIMIT


def _expand_details_arxiv(article: Article) -> Article:
    # previous state is 0
    article.State = 1  # next state
    # backward_state = 0

    # Archive is One Shot. There is no need for this step,
    # although it should be checked why it is at this step
    return article


def _expand_details_pubmed(article: Article) -> Article:
    # previous state is 0
    article.State = 1  # next state
    backward_state = 0
    sleep_time = 1 / tps_limit
    time.sleep(sleep_time)
    try:
        oa = get_article_details_from_pubmed(article.PMID)
        article.OreginalArticle = oa
    except Exception:
        article.State = backward_state
        print_error()

    return article


def expand_details(article: Article) -> Article:
    # this is dispatcher function
    if article.SourceBank is None:
        # This is Pubmed
        updated_article = _expand_details_pubmed(article)
    elif article.SourceBank == SourceBankType.PUBMED:
        updated_article = _expand_details_pubmed(article)
    elif article.SourceBank == SourceBankType.ARXIV:
        updated_article = _expand_details_arxiv(article)
    else:
        raise NotImplementedError

    return updated_article
