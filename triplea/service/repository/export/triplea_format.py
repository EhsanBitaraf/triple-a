import json
import sys

import click
from triplea.service.click_logger import logger
from triplea.schemas.article import Article
import triplea.service.repository.persist as persist
import traceback



def export_triplea_json(proccess_bar=False, limit_sample=0)-> str:
    print(limit_sample)
    l_pmid = persist.get_all_article_pmid_list()
    logger.DEBUG(f"{str(len(l_pmid))} Article(s) Selected.")

    total_article_in_current_state = len(l_pmid)
    n = 0

    if proccess_bar:
        bar = click.progressbar(length=len(l_pmid), show_pos=True, show_percent=True)

    refresh_point = 0

    output = []
    for id in l_pmid:
        try:
            n = n + 1
            if refresh_point == 50:
                refresh_point = 0
                print()
                logger.INFO(
                    f"There are {str(total_article_in_current_state - n)} article(s) left ... ",
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
            #------------------Select ----------------
            output.append (updated_article)
            if proccess_bar:
                bar.label = (
                    "Article "
                    + id
                    + " exported. "
                )
                bar.update(1)            
            if limit_sample == 0: # unlimited
                pass
            else:
                if n > limit_sample:
                    break
            #------------------Select ----------------
        except Exception:
                exc_type, exc_value, exc_tb = sys.exc_info()
                print()
                print(exc_tb.tb_lineno)
                logger.ERROR(f"Error {exc_type}")
                logger.ERROR(f"Error {exc_value}")
                traceback.print_tb(exc_tb)

    final = json.dumps(output, default=lambda o: o.__dict__, indent=2)
    print()
    logger.INFO("Export Complete.")
    return final

