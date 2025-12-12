from typing import Optional
import click
from triplea.config.settings import SETTINGS
# from triplea.service.click_logger import logger
from triplea.schemas.article import Article, SourceBankType
from triplea.service.repository.pipeline_core.__move_article_state_forward_by_id import move_article_state_forward_by_id
import triplea.service.repository.state as state_manager
import triplea.service.repository.persist as persist
from triplea.utils.general import print_error
from triplea.utils.general import get_tqdm
tps_limit = SETTINGS.AAA_TPS_LIMIT

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

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
    l_id = persist.get_article_id_list_by_state(state)
    total_article_in_current_state = len(l_id)
    n = 0
    logger.info(str(len(l_id)) + " Article(s) is in state " + str(state))

    tqdm = get_tqdm()
    bar = tqdm(total=len(l_id), desc="Processing ")
    refresh_point = 0
    for id in l_id:
        try:
            n = n + 1
            current_state = None

            if refresh_point == SETTINGS.AAA_CLI_ALERT_POINT:
                refresh_point = 0
                persist.refresh()
                logger.info(
                    f"There are {str(total_article_in_current_state - n)} article(s) left "
                )
            else:
                refresh_point = refresh_point + 1

            # process article with handeling state when error happend
            move_article_state_forward_by_id(id)

            bar.set_description(f"Article {id} process")   
            bar.update(1)

        except Exception as e:
            logger.error(f"Criticl Error hppend with article {id} but move next : {e}" , exc_info=True)

    logger.debug("update database.")
    persist.refresh()
    bar.close()