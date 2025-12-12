from triplea.schemas.article import Article, Author
# from triplea.service.click_logger import logger
import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def _parse_arxiv_author(single_author_dict: dict) -> Author:
    a = Author()
    a.FullName = single_author_dict["name"]
    logger.warning("TODO affilation in _parse_arxiv_author")
    # TODO affilation
    return a


def parsing_details_arxiv(article: Article) -> Article:
    # current state may be 1
    article.State = 2  # next state
    backward_state = -1
    data = article.OreginalArticle

    if data is None:
        print()
        logger.error(
            f"""Error in Original Article data. It is Null.
            PMID = {article.ArxivID}"""
        )
        article.State = backward_state
        return article

    try:
        article.Journal = "Arxiv"
        article.Title = str(data["title"]).replace("\n", " ")
        article.Abstract = str(data["summary"]).replace("\n", " ")

        if isinstance(data["author"], list):
            article_author_list = []
            for auth in data["author"]:
                article_author_list.append(_parse_arxiv_author(auth))
        else:
            article_author_list = []
            article_author_list.append(_parse_arxiv_author(data["author"]))

        article.Authors = article_author_list

        article.Published = data["published"]
        # This is helped
        # http://lukasschwab.me/arxiv.py/arxiv.html#Result.get_short_id

        # TODO DOI
        return article
    except Exception as e:
        article.State = backward_state
        logger.error(f"Error in parsing_details_arxiv : {e}" , exc_info=True)
        return article
