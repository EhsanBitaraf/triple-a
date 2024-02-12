import triplea.service.repository.persist as PERSIST
import click
from triplea.schemas.article import Article
from triplea.utils.general import print_error
from triplea.service.click_logger import logger


def reset_flag_llm_by_function(TemplateID, fx, limit_sample=0, proccess_bar=True):
    l_id = PERSIST.get_article_id_list_by_cstate(1, "FlagShortReviewByLLM")
    n = 0
    change_number = 0
    doc_number = len(l_id)
    if doc_number == 0:
        return
    if proccess_bar:
        bar = click.progressbar(length=doc_number, show_pos=True, show_percent=True)

    for id in l_id:
        n = n + 1
        try:
            a = PERSIST.get_article_by_id(id)
            article = Article(**a.copy())
            if fx(TemplateID, article.ReviewLLM) is True:
                # Change FlagShortReviewByLLM to 1
                PERSIST.update_cstate_by_id(id, "FlagShortReviewByLLM", 0)
                change_number = change_number + 1

            if proccess_bar:
                bar.label = f"""{change_number} Article(s) Updated."""
                bar.update(1)

            if limit_sample != 0:  # Unlimited
                if n > limit_sample:
                    break
        except Exception:
            print()
            print(logger.ERROR(f"article. ID = {id}"))
            print_error()
