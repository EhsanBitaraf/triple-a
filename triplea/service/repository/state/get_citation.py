import sys
from triplea.client.pubmed import get_cited_article_from_pubmed
from triplea.schemas.article import Article
from triplea.service.click_logger import logger



def get_citation(article: Article):
    """
    It takes an article, checks if the article's CiteCrawlerDeep is greater than 0, tries to get the cited articles from PubMed,
    sets the article's CitedBy to the cited articles, logs that new articles are being added, creates a new CiteCrawlerDeep,
    loops through the cited articles, and inserts the new PMID and CiteCrawlerDeep

    :param article: Article
    :type article: Article
    :return: Article with list of CitedBy
    """
    article.State = 3
    pmid = article.PMID
    if pmid is not None:
        if article.CiteCrawlerDeep is None:
            article.CiteCrawlerDeep = 0
        if article.CiteCrawlerDeep > 0:
            try:
                lc = get_cited_article_from_pubmed(pmid)
            except Exception:
                article.State = 3
                exc_type, exc_value, exc_tb = sys.exc_info()
                logger.ERROR(f"Error {exc_type} Value : {exc_value}")
                logger.ERROR(f"Error {exc_tb}")
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
                        new_ccd = article.CiteCrawlerDeep - 1
                        # CRITICAL Temporary Disable
                        # for c in lc:
                        #     persist.insert_new_pmid(pmid=c, cite_crawler_deep=new_ccd)
        else:
            pass
            article.State = 3
            # logger.DEBUG(f'Article {pmid} Cite Crawler Deep = {article.CiteCrawlerDeep}.'  , deep = 5)
    return article
