
import click
from triplea.config.settings import SETTINGS
from triplea.schemas.article import Article
import triplea.service.repository.persist as persist
import triplea.service.repository.state as state_manager
from triplea.service.click_logger import logger
from triplea.utils.general import print_error
from triplea.utils.general import get_tqdm



def go_extract_triple(proccess_bar=True):
    # max_refresh_point = SETTINGS.AAA_CLI_ALERT_POINT
    l_id = persist.get_article_id_list_by_cstate(0, "FlagExtractKG")
    total_article_in_current_state = len(l_id)
    n = 0
    logger.DEBUG(str(len(l_id)) + " Article(s) is in FlagExtractKG " + str(0))

    if proccess_bar:
        bar = click.progressbar(length=len(l_id), show_pos=True, show_percent=True)

    refresh_point = 0
    for id in l_id:
        try:
            n = n + 1
            current_state = None

            if refresh_point == SETTINGS.AAA_CLI_ALERT_POINT:
                refresh_point = 0
                persist.refresh()
                if proccess_bar:
                    print()
                    logger.INFO(
                        f"There are {str(total_article_in_current_state - n)} article(s) left ",  # noqa: E501
                        forecolore="yellow",
                    )
                if proccess_bar is False:
                    bar.label = f"There are {str(total_article_in_current_state - n)} article(s) left "  # noqa: E501
                    bar.update(SETTINGS.AAA_CLI_ALERT_POINT)
            else:
                refresh_point = refresh_point + 1

            a = persist.get_article_by_id(id)
            try:
                updated_article = Article(**a.copy())
            except Exception:
                print()
                print(logger.ERROR(f"Error in parsing article. ID = {id}"))
                raise Exception("Article Not Parsed.")
            try:
                current_state = updated_article.FlagExtractKG
            except Exception:
                current_state = 0

            if proccess_bar:
                bar.label = (
                    "Article " + str(id) + " Extract Knowledge Triple From Abstract"
                )
                bar.update(1)

            if current_state is None:
                updated_article = state_manager.extract_triple_abstract_save(
                    updated_article, id
                )
                persist.update_article_by_id(updated_article, id)

            elif current_state == -1:
                updated_article = state_manager.extract_triple_abstract_save(
                    updated_article, id
                )
                persist.update_article_by_id(updated_article, id)

            elif current_state == 0:
                updated_article = state_manager.extract_triple_abstract_save(
                    updated_article, id
                )
                persist.update_article_by_id(updated_article, id)

            elif current_state == 1:
                pass

            else:
                raise NotImplementedError

        except Exception:
            if current_state == 0 or current_state is None:
                updated_article = Article(**a.copy())
                updated_article.FlagExtractKG = 0  # -----------------
                persist.update_article_by_id(updated_article, id)
                persist.refresh()
                print_error()

            else:
                persist.refresh()
                print_error()

    persist.refresh()

