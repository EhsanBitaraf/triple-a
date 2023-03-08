# from triplea.config.settings import SETTINGS,DB_ROOT_PATH
import sys
from typing import Optional

import click
from triplea.db.mongodb import DB_MongoDB
from triplea.db.tinydb import DB_TinyDB
from triplea.schemas.article import Article
from triplea.service.click_logger import logger


def convert_arepo_mongodb_to_tinydb(
    move_oreginal_article: Optional[bool] = False, state: Optional[int] = 2
):
    source_db = DB_MongoDB()
    l_pmid = source_db.get_article_pmid_list_by_state(state)
    article_count = len(l_pmid)
    if article_count > 10000:
        pass
        # raise NotImplementedError

    logger.DEBUG(str(len(l_pmid)) + " Article(s) is in state " + str(state))

    destination_db = DB_TinyDB()

    bar = click.progressbar(length=article_count, show_pos=True, show_percent=True)
    n = 0
    for id in l_pmid:
        a = source_db.get_article_by_pmid(id)
        pmid = a["PMID"]
        if destination_db.is_article_exist_by_pmid(pmid):
            # logger.INFO(f'The article {pmid} already exists.', deep = 3 )
            bar.label = f"The article {pmid} already exists."
        else:
            n = n + 1
            try:
                if move_oreginal_article is False:
                    a["OreginalArticle"] = {}
                    a = Article(**a.copy())
                else:
                    a = Article(**a.copy())

                destination_db.add_new_article(a)
            except Exception:
                print()
                logger.ERROR(
                    f"The copy of article {pmid} encountered an error.", deep=3
                )
                exc_type, exc_value, exc_tb = sys.exc_info()
                logger.ERROR(f"Error {exc_type}", deep=3)
                logger.ERROR(f"Error {exc_value}", deep=3)

            # logger.DEBUG(f'{n} Copy article {pmid} to destination repository.', deep = 3 )
            bar.label = f"{n} Copy article {pmid} to destination repository."
        bar.update(1)


def convert_arepo_tinydb_to_mongodb():
    source_db = DB_TinyDB()
    article_count = source_db.get_all_article_count()
    if article_count > 10000:
        pass
        # raise NotImplementedError

    la = source_db.get_article_by_state(0)
    destination_db = DB_MongoDB()
    n = 0
    for a in la:
        pmid = a["PMID"]
        if destination_db.is_article_exist_by_pmid(pmid):
            logger.INFO(f"The article {pmid} already exists.", deep=3)
        else:
            n = n + 1
            destination_db.add_new_article(a)
            logger.DEBUG(f"{n} Copy article {pmid} to destination repository.", deep=3)


if __name__ == "__main__":
    pass
    # convert_arepo_mongodb_to_tinydb(state = 2)

    # convert()
    # convert_to_neo4j()

    # destination_db = DB_MongoDB()
    # print(destination_db.get_all_article_count())
    # la = destination_db.get_article_by_state(3)
    # for a in la:
    #     print(a)

    # a = destination_db.get_article_by_pmid('36715845')
    # a = destination_db.is_article_exist_by_pmid('36715845')
    # print(type(a))
    # print(a)
    # destination_db.col_article.drop()
