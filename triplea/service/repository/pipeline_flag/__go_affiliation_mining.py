import click
from triplea.config.settings import SETTINGS
from triplea.schemas.article import Article
import triplea.service.repository.persist as persist
import triplea.service.repository.state as state_manager
from triplea.service.click_logger import logger
from triplea.utils.general import print_error
from triplea.utils.general import get_tqdm

def go_affiliation_mining(method: str = "Simple",
                         proccess_bar=True,
                         limit_sample=0):

    # max_refresh_point = SETTINGS.AAA_CLI_ALERT_POINT
    l_id = persist.get_article_id_list_by_cstate(0, "FlagAffiliationMining")
    # total_article_in_current_state = len(l_id)
    doc_number = len(l_id)
    n = 0
    logger.DEBUG(
        f"""{str(
                len(l_id)
                )} Article(s) is in FlagAffiliationMining {str(0)}"""
    )

    if proccess_bar:
        # bar = click.progressbar(length=doc_number,
        #                         show_pos=True,
        #                         show_percent=True)
        tqdm = get_tqdm()
        bar = tqdm(total=doc_number, desc="Processing ")
    else:
        logger.INFO("Start ...")

    for id in l_id:
        try:
            n = n + 1
            current_state = None

            # # -----------------------------Temporary------------------------
            # from bson import ObjectId
            # id = "65d46589604437efd5da91cd"
            # id = ObjectId(id)
            # # -----------------------------Temporary------------------------
            a = persist.get_article_by_id(id)
            try:
                updated_article = Article(**a.copy())
            except Exception:
                print()
                print(logger.ERROR(f"Error in parsing article. ID = {id}"))
                raise Exception("Article Not Parsed.")
            try:
                current_state = updated_article.FlagAffiliationMining
            except Exception:
                current_state = 0

            # For View Proccess
            if proccess_bar:
                # bar.label = f"Article {id} affiliation mining."
                bar.set_description( f"Article {id} affiliation mining.")
                bar.update(1)
            else:
                if n % SETTINGS.AAA_CLI_ALERT_POINT == 0:
                    logger.INFO(f"{n} Article(s) affiliation mining..")
                persist.refresh()

            if limit_sample != 0:  # Unlimited
                if n > limit_sample:
                    break

            if current_state is None or current_state == -1 or current_state == 0:
                if method == "Simple":
                    updated_article = state_manager.affiliation_mining(updated_article)
                    persist.update_article_by_id(updated_article, id)
                elif method == "Titipata":
                    updated_article = state_manager.affiliation_mining_titipata(
                        updated_article
                    )
                    persist.update_article_by_id(updated_article, id)
                elif method == "TitipataIntegrated":
                    updated_article = (
                        state_manager.affiliation_mining_titipata_integration(
                            updated_article
                        )
                    )
                    persist.update_article_by_id(updated_article, id)
                elif method == "RegexIntegrated":
                    updated_article = (
                        state_manager.affiliation_mining_regex_integration(
                            updated_article
                        )
                    )
                    persist.update_article_by_id(updated_article, id)

            elif current_state == 1:
                pass

            else:
                raise NotImplementedError

        except Exception:
            if current_state == 0 or current_state is None:
                updated_article = Article(**a.copy())
                updated_article.FlagAffiliationMining = -1
                persist.update_article_by_id(updated_article, id)
                persist.refresh()
                print_error()

            else:
                persist.refresh()
                print_error()
    persist.refresh()
    bar.close()

