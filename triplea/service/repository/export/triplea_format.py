import json
import sys
from triplea.service.click_logger import logger
from triplea.schemas.article import Article
import triplea.service.repository.persist as persist
import traceback



def export_triplea_json()-> str:
    l_pmid = persist.get_all_article_pmid_list()
    logger.DEBUG(f"{str(len(l_pmid))} Article(s) Selected.")

    total_article_in_current_state = len(l_pmid)
    number_of_article_move_forward = 0

    refresh_point = 0
    n = 0
    output = []
    for id in l_pmid:
        try:
            number_of_article_move_forward = number_of_article_move_forward + 1
            if refresh_point == 50:
                refresh_point = 0
                print()
                logger.INFO(
                    f"There are {str(total_article_in_current_state - number_of_article_move_forward)} article(s) left ... ",
                    forecolore="yellow",
                )
                break # for test first 500
            else:
                refresh_point = refresh_point + 1

            a = persist.get_article_by_pmid(id)
            try:
                updated_article = Article(**a.copy())
            except Exception:
                print()
                print(logger.ERROR(f"Error in parsing article. PMID = {id}"))
                raise Exception("Article Not Parsed.")
            #------------------Select ----------------
            n=n+1
            output.append (updated_article)

            #------------------Select ----------------
        except Exception:
                exc_type, exc_value, exc_tb = sys.exc_info()
                print()
                print(exc_tb.tb_lineno)
                logger.ERROR(f"Error {exc_type}")
                logger.ERROR(f"Error {exc_value}")
                traceback.print_tb(exc_tb)

    final = json.dumps(output, default=lambda o: o.__dict__, indent=2)
    output
    logger.INFO("Export Complete.")
    return final

