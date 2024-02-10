from typing import Optional
import click
from triplea.config.settings import SETTINGS
from triplea.service.click_logger import logger
from triplea.schemas.article import Article, SourceBankType
import triplea.service.repository.state as state_manager
import triplea.service.repository.persist as persist
from triplea.utils.general import print_error

tps_limit = SETTINGS.AAA_TPS_LIMIT


def move_state_until(end_state: int):
    l_pmid = persist.get_all_article_pmid_list()
    logger.INFO(str(len(l_pmid)) + " Article(s) is arepo ")

    bar = click.progressbar(length=len(l_pmid), show_pos=True, show_percent=True)

    for id in l_pmid:
        updated_article_current_state = None
        a = persist.get_article_by_pmid(id)
        try:
            updated_article = Article(**a.copy())
        except Exception:
            print()
            logger.ERROR(f"Error in parsing article. PMID = {id}")
            # raise Exception('Article Not Parsed.')

        updated_article_current_state = updated_article.State

        for current_state in range(updated_article_current_state, 3):
            if current_state is None:
                updated_article = state_manager.expand_details(updated_article)

            elif current_state == -1:  # Error in State 0 Net state: 1
                updated_article = state_manager.parsing_details(updated_article)

            elif current_state == 0:  # Net state: get article details from pubmed
                updated_article = state_manager.expand_details(updated_article)

            elif current_state == 1:  # Net state: Extract Data
                updated_article = state_manager.parsing_details(updated_article)

            elif current_state == 2:  # Next state: Get Citation
                updated_article = state_manager.get_citation(updated_article)

            elif current_state == -2:  # Next state: Get Citation
                updated_article = state_manager.get_citation(updated_article)

            elif current_state == 3:  # Next state: Get Full Text
                updated_article = state_manager.get_full_text(updated_article)

            elif current_state == -3:  # Next state: Get Full Text
                updated_article = state_manager.get_full_text(updated_article)

            else:
                raise NotImplementedError

        persist.update_article_by_id(updated_article, id)
        bar.label = f"Article {updated_article.PMID} with state {str(updated_article_current_state)} forward to {str(end_state)}"  # noqa: E501
        bar.update(1)
    persist.refresh()


def move_state_forward(  # noqa: C901
    state: int,
    tps_limit: Optional[int] = 1,
    extend_by_refrence: Optional[bool] = False,
    extend_by_cited: Optional[bool] = False,
):
    """
    It takes an article, extracts the data from it,
      and then creates a node and edge for each author and
    affiliation

    :param state: The state of the article in Knowledge Repository
      you want to move forward
    :type state: int
    :param tps_limit: The number of requests per second
      you want to make to the API, defaults to 1
    :type tps_limit: Optional[int] (optional)
    """
    # old version
    # la = get_article_by_state(state)

    # old version 0.0.3
    # l_pmid = persist.get_article_pmid_list_by_state(state)
    l_id = persist.get_article_id_list_by_state(state)
    total_article_in_current_state = len(l_id)
    n = 0
    logger.DEBUG(str(len(l_id)) + " Article(s) is in state " + str(state))

    bar = click.progressbar(length=len(l_id), show_pos=True, show_percent=True)

    refresh_point = 0
    for id in l_id:
        try:
            n = n + 1
            current_state = None

            if refresh_point == SETTINGS.AAA_CLI_ALERT_POINT:
                refresh_point = 0
                persist.refresh()
                print()
                logger.INFO(
                    f"There are {str(total_article_in_current_state - n)} article(s) left ",  # noqa: E501
                    forecolore="yellow",
                )
            else:
                refresh_point = refresh_point + 1

            a = persist.get_article_by_id(id)
            # CRITICAL For Test and Debug
            # a = persist.get_article_by_pmid('8099394')

            try:
                updated_article = Article(**a.copy())
            except Exception:
                print()
                print(logger.ERROR(f"Error in parsing article with ID = {id}"))
                raise Exception("Article Not Parsed.")

            try:
                current_state = updated_article.State
            except Exception:
                current_state = 0

            source_bank = updated_article.SourceBank

            if source_bank is None:
                article_source_bank_title = "Pubmed"
                article_identifier = updated_article.PMID
                source_bank = SourceBankType.PUBMED
            elif source_bank == SourceBankType.PUBMED:
                article_source_bank_title = "Pubmed"
                article_identifier = updated_article.PMID
            elif source_bank == SourceBankType.ARXIV:
                article_source_bank_title = "Arxiv"
                article_identifier = updated_article.ArxivID
            else:
                raise NotImplementedError

            bar.label = f"Article {article_source_bank_title} ({article_identifier}) with state {str(current_state)} forward to {str(current_state + 1)}"  # noqa: E501
            bar.update(1)
            # # for re run
            # if current_state == 2 : current_state = 1

            if current_state is None:
                updated_article = state_manager.expand_details(updated_article)

            elif current_state == 0:  # Next state: get article details from pubmed
                updated_article = state_manager.expand_details(updated_article)

            elif current_state == 1:  # Next state: Extract Data
                updated_article = state_manager.parsing_details(updated_article)

            elif current_state == -1:  # Error in State 0 Next state: 1
                updated_article = state_manager.parsing_details(updated_article)

            elif current_state == 2:  # Next state: Get Citation
                updated_article = state_manager.get_citation(updated_article)

            elif current_state == -2:  # Next state: Get Citation
                updated_article = state_manager.get_citation(updated_article)

            elif current_state == 3:  # Next state: Get Full Text
                updated_article = state_manager.get_full_text(updated_article)

            elif current_state == -3:  # Next state: Get Full Text
                updated_article = state_manager.get_full_text(updated_article)

            elif current_state == 4:  # Next state: Convert Full Text
                updated_article = state_manager.convert_full_text2string(
                    updated_article
                )

            elif current_state == -4:  # Next state: Convert Full Text
                updated_article = state_manager.convert_full_text2string(
                    updated_article
                )

            else:
                print()
                logger.ERROR("Error undefine current state.")

            persist.update_article_by_id(updated_article, id)

        except Exception:
            if current_state == 1:
                updated_article = Article(**a.copy())
                updated_article.State = -1
                persist.update_article_by_id(updated_article, id)
                persist.refresh()
                print_error()

            elif current_state is None:
                # Article Not Parsed.
                persist.refresh()
                print_error()

            elif current_state == 2:
                updated_article = Article(**a.copy())
                updated_article.State = -2
                persist.update_article_by_id(updated_article, id)
                persist.refresh()
                print_error()

            else:
                persist.refresh()
                print_error()

    persist.refresh()
