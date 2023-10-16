import sys
import time
import traceback
import click
from triplea.schemas.article import Article
import triplea.service.repository.persist as persist
import triplea.service.repository.state as state_manager
from triplea.service.click_logger import logger


def go_extract_triple():
    online_bar = True
    max_refresh_point = 500
    l_pmid = persist.get_article_pmid_list_by_cstate(0, "FlagExtractKG")
    total_article_in_current_state = len(l_pmid)
    number_of_article_move_forward = 0
    logger.DEBUG(str(len(l_pmid)) + " Article(s) is in FlagExtractKG " + str(0))

    bar = click.progressbar(length=len(l_pmid), show_pos=True, show_percent=True)

    refresh_point = 0
    for id in l_pmid:
        try:
            number_of_article_move_forward = number_of_article_move_forward + 1
            current_state = None

            if refresh_point == max_refresh_point:
                refresh_point = 0
                persist.refresh()
                if online_bar:
                    print()
                    logger.INFO(
                        f"There are {str(total_article_in_current_state - number_of_article_move_forward)} article(s) left ",
                        forecolore="yellow",
                    )
                if online_bar is False:
                    bar.label = f"There are {str(total_article_in_current_state - number_of_article_move_forward)} article(s) left "
                    bar.update(max_refresh_point)
            else:
                refresh_point = refresh_point + 1

            a = persist.get_article_by_pmid(id)
            try:
                updated_article = Article(**a.copy())
            except Exception:
                print()
                print(logger.ERROR(f"Error in parsing article. PMID = {id}"))
                raise Exception("Article Not Parsed.")
            try:
                current_state = updated_article.FlagExtractKG
            except Exception:
                current_state = 0

            if online_bar:
                bar.label = (
                    "Article "
                    + updated_article.PMID
                    + " Extract Knowledge Triple From Abstract"
                )
                bar.update(1)

            if current_state is None:
                updated_article = state_manager.extract_triple_abstract_save(
                    updated_article
                )
                persist.update_article_by_pmid(updated_article, updated_article.PMID)

            elif current_state == -1:
                updated_article = state_manager.extract_triple_abstract_save(
                    updated_article
                )
                persist.update_article_by_pmid(updated_article, updated_article.PMID)

            elif current_state == 0:
                updated_article = state_manager.extract_triple_abstract_save(
                    updated_article
                )
                persist.update_article_by_pmid(updated_article, updated_article.PMID)

            elif current_state == 1:
                pass

            else:
                raise NotImplementedError

        except Exception:
            if current_state == 0 or current_state is None:
                updated_article = Article(**a.copy())
                updated_article.FlagExtractKG = 0
                persist.update_article_by_pmid(updated_article, updated_article.PMID)
                persist.refresh()
                exc_type, exc_value, exc_tb = sys.exc_info()
                print()
                logger.ERROR(f"Error {exc_type}")
                logger.ERROR(f"Error {exc_value}")

            else:
                persist.refresh()
                exc_type, exc_value, exc_tb = sys.exc_info()
                print()
                print(exc_tb.tb_lineno)
                print()
                traceback.print_tb(exc_tb)
                logger.ERROR(f"Error {exc_type}")
                logger.ERROR(f"Error {exc_value}")
                logger.ERROR(f"Error {exc_tb}")
    persist.refresh()


def go_extract_topic(proccess_bar=True):
    max_refresh_point = 100
    l_pmid = persist.get_article_pmid_list_by_cstate(0, "FlagExtractTopic")
    total_article_in_current_state = len(l_pmid)
    n = 0
    logger.DEBUG(str(len(l_pmid)) + " Article(s) is in FlagExtractTopic " + str(0))

    if proccess_bar:
        bar = click.progressbar(length=len(l_pmid), show_pos=True, show_percent=True)

    refresh_point = 0

    for id in l_pmid:
        try:
            n = n + 1
            current_state = None

            if refresh_point == max_refresh_point:
                refresh_point = 0
                persist.refresh()
                if proccess_bar:
                    print()
                    logger.INFO(
                        f"There are {str(total_article_in_current_state - n)} article(s) left ",
                        forecolore="yellow",
                    )
                if proccess_bar is False:
                    bar.label = f"There are {str(total_article_in_current_state - n)} article(s) left "
                    bar.update(max_refresh_point)
            else:
                refresh_point = refresh_point + 1

            a = persist.get_article_by_pmid(id)
            try:
                updated_article = Article(**a.copy())
            except Exception:
                print()
                print(logger.ERROR(f"Error in parsing article. PMID = {id}"))
                raise Exception("Article Not Parsed.")
            try:
                current_state = updated_article.FlagExtractTopic  # ------------
            except Exception:
                current_state = 0

            if proccess_bar:
                bar.label = (
                    "Article " + updated_article.PMID + " , topic were extracted."
                )
                bar.update(1)

            if current_state is None:
                updated_article = state_manager.extract_topic_abstract(updated_article)
                persist.update_article_by_pmid(updated_article, updated_article.PMID)

            elif current_state == -1:
                updated_article = state_manager.extract_topic_abstract(updated_article)
                persist.update_article_by_pmid(updated_article, updated_article.PMID)

            elif current_state == 0:
                updated_article = state_manager.extract_topic_abstract(updated_article)
                persist.update_article_by_pmid(updated_article, updated_article.PMID)

            elif current_state == 1:
                pass

            else:
                raise NotImplementedError

        except Exception:
            if current_state == 0 or current_state is None:
                updated_article = Article(**a.copy())
                updated_article.FlagExtractTopic = -1
                persist.update_article_by_pmid(updated_article, updated_article.PMID)
                persist.refresh()
                exc_type, exc_value, exc_tb = sys.exc_info()
                print()
                logger.ERROR(f"Error {exc_type}")
                logger.ERROR(f"Error {exc_value}")

            else:
                persist.refresh()
                exc_type, exc_value, exc_tb = sys.exc_info()
                print()
                print(exc_tb.tb_lineno)
                logger.ERROR(f"Error {exc_type}")
                logger.ERROR(f"Error {exc_value}")
    persist.refresh()


def go_affiliation_mining(method: str = "Simple"):
    l_pmid = persist.get_article_pmid_list_by_cstate(0, "FlagAffiliationMining")
    total_article_in_current_state = len(l_pmid)
    number_of_article_move_forward = 0
    logger.DEBUG(str(len(l_pmid)) + " Article(s) is in FlagAffiliationMining " + str(0))

    bar = click.progressbar(length=len(l_pmid), show_pos=True, show_percent=True)

    refresh_point = 0
    elapsed = 0
    for id in l_pmid:
        start_time = time.time()
        try:
            number_of_article_move_forward = number_of_article_move_forward + 1
            current_state = None

            if refresh_point == 50:
                refresh_point = 0
                persist.refresh()
                print()
                logger.INFO(
                    f"There are {str(total_article_in_current_state - number_of_article_move_forward)} article(s) left ",
                    forecolore="yellow",
                )
                min = (
                    (total_article_in_current_state - number_of_article_move_forward)
                    * elapsed
                ) / 60
                logger.INFO(
                    f"It takes at least {str(int(min))} minutes or {str(int(min/60))} hours",
                    forecolore="yellow",
                )
            else:
                refresh_point = refresh_point + 1

            a = persist.get_article_by_pmid(id)
            try:
                updated_article = Article(**a.copy())
            except Exception:
                print()
                print(logger.ERROR(f"Error in parsing article. PMID = {id}"))
                raise Exception("Article Not Parsed.")
            try:
                current_state = updated_article.FlagAffiliationMining
            except Exception:
                current_state = 0

            # logger.DEBUG('Article ' + updated_article.PMID + ' with state ' + str(current_state) + ' forward to ' + str(current_state + 1))
            bar.label = "Article " + updated_article.PMID + " affiliation mining."
            bar.update(1)
            # # for re run
            # if current_state == 2 : current_state = 1

            if current_state is None or current_state == -1 or current_state == 0:
                if method == "Simple":
                    updated_article = state_manager.affiliation_mining(updated_article)
                    persist.update_article_by_pmid(
                        updated_article, updated_article.PMID
                    )
                elif method == "Titipata":
                    updated_article = state_manager.affiliation_mining_titipata(
                        updated_article
                    )
                    persist.update_article_by_pmid(
                        updated_article, updated_article.PMID
                    )

            elif current_state == 1:
                pass

            else:
                raise NotImplementedError

        except Exception:
            if current_state == 0 or current_state is None:
                updated_article = Article(**a.copy())
                updated_article.State = -1
                persist.update_article_by_pmid(updated_article, updated_article.PMID)
                persist.refresh()
                exc_type, exc_value, exc_tb = sys.exc_info()
                print()
                logger.ERROR(f"Error {exc_type}")
                logger.ERROR(f"Error {exc_value}")

            else:
                persist.refresh()
                exc_type, exc_value, exc_tb = sys.exc_info()
                print()
                print(exc_tb.tb_lineno)
                logger.ERROR(f"Error {exc_type}")
                logger.ERROR(f"Error {exc_value}")
        elapsed = time.time() - start_time
    persist.refresh()
