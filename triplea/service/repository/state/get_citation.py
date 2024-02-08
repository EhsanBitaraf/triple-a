from triplea.client.pubmed import get_cited_article_from_pubmed
from triplea.schemas.article import Article, SourceBankType
from triplea.service.click_logger import logger
from triplea.utils.general import print_error


def _get_citation_pubmed(article: Article):
    """
    It takes an article, checks if the article's CiteCrawlerDeep
      is greater than 0, tries to get the cited articles from PubMed,
    sets the article's CitedBy to the cited articles, logs that new articles
      are being added, creates a new CiteCrawlerDeep,
    loops through the cited articles,
      and inserts the new PMID and CiteCrawlerDeep

    :param article: Article
    :type article: Article
    :return: Article with list of CitedBy
    """
    # previous state is 2
    article.State = 3  # next state
    backward_state = -2

    try:
        pmid = article.PMID
        if pmid is not None:
            if article.CiteCrawlerDeep is None:
                article.CiteCrawlerDeep = 0
            if article.CiteCrawlerDeep > 0:
                try:
                    lc = get_cited_article_from_pubmed(pmid)
                except Exception:
                    article.State = backward_state
                    print_error()
                    return article

                if lc is not None:
                    if len(lc) > 0:
                        if article.CiteCrawlerDeep is None:
                            article.CiteCrawlerDeep = 0
                            # raise Exception('CiteCrawlerDeep is None.')
                        if article.CiteCrawlerDeep > 0:
                            article.CitedBy = lc
                            # create new article
                            logger.DEBUG(
                                f"Add {len(lc)} new article(s) by CITED.",
                                forecolore="yellow",
                                deep=3,
                            )
                            # new_ccd = article.CiteCrawlerDeep - 1
                            # CRITICAL Temporary Disable for crawle Citation.
                            # for c in lc:
                            #     persist.insert_new_pmid(pmid=c,
                            #                            cite_crawler_deep=new_ccd)
            else:
                pass
                article.State = 3
                logger.DEBUG(
                    f"""Article {pmid} Cite
                                Crawler Deep= {article.CiteCrawlerDeep}.""",
                    deep=5,
                )

        return article
    except Exception:
        print_error()
        article.State = backward_state
        return article


def _get_citation_arxiv(article: Article):
    # previous state is 2
    article.State = 3  # next state
    # backward_state = -2

    # I still haven't found an operational idea to get
    # citations of arxiv articles, maybe through google.
    return article


def get_citation(article: Article):
    # this is dispatcher function
    if article.SourceBank is None:
        # This is Pubmed
        updated_article = _get_citation_pubmed(article)
    elif article.SourceBank == SourceBankType.PUBMED:
        updated_article = _get_citation_pubmed(article)
    elif article.SourceBank == SourceBankType.ARXIV:
        updated_article = _get_citation_arxiv(article)
    else:
        raise NotImplementedError

    return updated_article
