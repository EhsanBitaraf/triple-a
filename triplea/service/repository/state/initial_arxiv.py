import json
from triplea.client.arxiv import get_article_list_from_arxiv
from triplea.schemas.article import Article, SourceBankType
from triplea.service.click_logger import logger
from triplea.config.settings import SETTINGS
import triplea.service.repository.persist as persist

import time
from typing import Optional

from triplea.utils.general import print_error


def parse_arxiv_list(data: dict):
    article_list = []
    try:
        if "feed" not in data:
            print()
            logger.ERROR("Error in parsing arxiv response. Feed missing.")
        if "entry" not in data["feed"]:
            print()
            logger.ERROR("Error in parsing arxiv response. Entry missing.")

        # Parse arxiv list into Article object list with State 1
        for a in data["feed"]["entry"]:
            article = Article()
            article.OreginalArticle = a
            article.SourceBank = SourceBankType.ARXIV
            article.QueryTranslation = data["feed"]["title"]["#text"]
            article.State = 1  # Because of ArXiv API  state 0,1 merge
            article.ReferenceCrawlerDeep = SETTINGS.AAA_REFF_CRAWLER_DEEP
            article.CiteCrawlerDeep = SETTINGS.AAA_CITED_CRAWLER_DEEP
            article.ArxivID = str(a["id"]).split("arxiv.org/abs/")[-1]

            article_list.append(article)
    except Exception:
        with open("error-parse_arxiv_list.json", "w") as outfile:
            outfile.write(json.dumps(data, indent=4, sort_keys=True))
            outfile.close()
        print_error()

    return article_list


def get_article_list_from_arxiv_all_store_to_arepo(
    searchterm: str,
    start: Optional[bool] = 1,
    max_results: Optional[int] = 100,
    tps_limit: Optional[int] = 1,  # tps_limit = 0 no limit
) -> None:
    if tps_limit == 0:
        sleep_time = 0
    else:
        sleep_time = 1 // tps_limit

    data = get_article_list_from_arxiv(searchterm, start, max_results)

    total = int(data["feed"]["opensearch:totalResults"]["#text"])
    logger.INFO("Total number of article is " + str(total))

    if total == 0:
        return

    article_list = parse_arxiv_list(data)

    for a in article_list:
        persist.insert_new_arxiv(a)
        persist.refresh()

    n = 0
    while start < total:
        n = n + 1
        start = start + max_results
        data = get_article_list_from_arxiv(searchterm, start, max_results)
        article_list = parse_arxiv_list(data)
        for a in article_list:
            persist.insert_new_arxiv(a)  # Check Dose Not Exist
        time.sleep(sleep_time)
        logger.INFO(
            f"""Round ({str(n)}) : Get another {str(
            max_results
            )}  record from {str(
                start
                )} to {str(
                    start + max_results
                    )} (Total {str(n * max_results)} record)""",
            deep=13,
        )
