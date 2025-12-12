from triplea.client.pubmed import get_cited_article_from_pubmed
from triplea.schemas.article import Article, SourceBankType
# from triplea.service.click_logger import logger
# from triplea.utils.general import print_error
import re
import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

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
                except Exception as e:
                    article.State = backward_state
                    logger.error(f"Error in _get_citation_pubmed : {e}" , exc_info=True)
                    return article

                if lc is not None:
                    if len(lc) > 0:
                        if article.CiteCrawlerDeep is None:
                            article.CiteCrawlerDeep = 0
                            # raise Exception('CiteCrawlerDeep is None.')
                        if article.CiteCrawlerDeep > 0:
                            article.CitedBy = lc
                            article.CitationCount = len(lc)
                            # create new article
                            logger.info(
                                f"Add {len(lc)} new article(s) by CITED."
                            )
                            # new_ccd = article.CiteCrawlerDeep - 1
                            # CRITICAL Temporary Disable for crawle Citation.
                            # for c in lc:
                            #     persist.insert_new_pmid(pmid=c,
                            #                            cite_crawler_deep=new_ccd)
            else:
                pass
                article.State = 3
                logger.debug(
                    f"""Article {pmid} Cite
                                Crawler Deep= {article.CiteCrawlerDeep}."""
                )

        return article
    except Exception as e:
        logger.error(f"Error in _get_citation_pubmed : {e}" , exc_info=True)
        article.State = backward_state
        return article


def _get_citation_arxiv(article: Article):
    # previous state is 2
    article.State = 3  # next state
    # backward_state = -2

    # I still haven't found an operational idea to get
    # citations of arxiv articles, maybe through google.
    return article


def _get_citation_ieee(article: Article):
    # previous state is 2
    article.State = 3  # next state
    # backward_state = -2

    # I still haven't found an operational idea to get
    # citations of IEEE RIS articles, maybe through google.
    return article


def _get_citation_wos(article: Article):
    # previous state is 2
    article.State = 3  # next state
    backward_state = -2
    ris_text = " ".join(article.OreginalArticle["file"])
    try:
        # Use re.MULTILINE to handle line starts
        pattern = re.compile(
            r"N1  -\s*(.*?)(?=(?:\n[A-Z]{2}  -)|\n\s+ER  -)", re.DOTALL | re.MULTILINE
        )
        n1_match = pattern.search(ris_text)

        if n1_match:
            n1_content = n1_match.group(1)

            # Extract specific counts
            times_cited_wos = re.search(
                r"Times Cited in Web of Science Core Collection:\s*(\d+)", n1_content
            )
            total_times_cited = re.search(r"Total Times Cited:\s*(\d+)", n1_content)
            cited_reference_count = re.search(
                r"Cited Reference Count:\s*(\d+)", n1_content
            )

            result = {
                "Times Cited in Web of Science Core Collection": (
                    int(times_cited_wos.group(1)) if times_cited_wos else None
                ),
                "Total Times Cited": (
                    int(total_times_cited.group(1)) if total_times_cited else None
                ),
                "Cited Reference Count": (
                    int(cited_reference_count.group(1))
                    if cited_reference_count
                    else None
                ),
            }
            article.CitationCount = int(result["Total Times Cited"])
            return article

        else:
            logger.warning("N1 field not found in WOS RIS Format.")
            logger.debug(ris_text)

    except Exception as e:
        logger.error(f"Error in _get_citation_wos : {e}" , exc_info=True)
        article.State = backward_state
        return article


def _get_citation_scopus(article: Article):
    # previous state is 2
    article.State = 3  # next state
    backward_state = -2
    ris_text = " ".join(article.OreginalArticle["file"])
    try:
        # Extract the ` N1` field
        n1_match = re.search(r"\n N1  - (.*?)\n", ris_text, re.DOTALL)
        if n1_match:
            n1_field = n1_match.group(1)
            # Extract 'Cited By: number'
            cited_by_match = re.search(r"Cited By:\s*(\d+)", n1_field)
            if cited_by_match:
                cited_by = cited_by_match.group(1)
                article.CitationCount = int(cited_by)
                return article
            else:
                print("Cited By not found in Scopus RIS Format.")
        else:
            print("N1 field not found in Scopus RIS Format.")
    except Exception as e:
        logger.error(f"Error in _get_citation_scopus : {e}" , exc_info=True)
        article.State = backward_state
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
    elif article.SourceBank == SourceBankType.IEEE:
        updated_article = _get_citation_ieee(article)
    elif article.SourceBank == SourceBankType.SCOPUS:
        updated_article = _get_citation_scopus(article)
    elif article.SourceBank == SourceBankType.WOS:
        updated_article = _get_citation_wos(article)
    elif article.SourceBank == SourceBankType.UNKNOWN:
        updated_article = _get_citation_ieee(article)
    elif article.SourceBank == SourceBankType.GOOGLESCHOLAR:
        updated_article = _get_citation_ieee(article)
    elif article.SourceBank == SourceBankType.EMBASE:
        updated_article = _get_citation_ieee(article)
    elif article.SourceBank == SourceBankType.ACM:
        updated_article = _get_citation_ieee(article)
    else:
        logger.error(f"NotImplementedError. Unrecognized rticle.SourceBank" )
        raise NotImplementedError

    return updated_article
