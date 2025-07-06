import triplea.service.repository.persist as PERSIST
import click
from triplea.schemas.article import Article
from triplea.utils.general import print_error
from triplea.service.click_logger import logger
from triplea.config.settings import SETTINGS


def export_engine(
    fx_filter, fx_transform, fx_output, limit_sample=0, proccess_bar=True
):
    # l_id = PERSIST.get_article_id_list_by_cstate(1, "FlagShortReviewByLLM")
    l_id = PERSIST.get_all_article_id_list()
    SETTINGS.AAA_CLI_ALERT_POINT
    n = 0
    filter_number = 0
    doc_number = len(l_id)
    if doc_number == 0:
        return
    if proccess_bar:
        bar = click.progressbar(length=doc_number, show_pos=True, show_percent=True)
    else:
        logger.INFO("Start export...")

    output_list = []
    for id in l_id:
        n = n + 1
        try:
            a = PERSIST.get_article_by_id(id)
            article = Article(**a.copy())
            model = None
            if fx_filter(article) is True:
                filter_number = filter_number + 1
                model = fx_transform(article)
                model["DBUID"] = id  # for expose id in export
            else:
                pass
                model = None
                # if fx_filter(article) is True:
                #     filter_number = filter_number + 1
                #     model = fx_transform(article)

            if model is not None:
                output_list.append(fx_output(model))

            # For View Proccess
            if proccess_bar:
                bar.label = f"""{filter_number} Article(s) exported."""
                bar.update(1)
            else:
                if n % SETTINGS.AAA_CLI_ALERT_POINT == 0:
                    logger.INFO(f"{n} Article(s) exported.")

            if limit_sample != 0:  # Unlimited
                if n > limit_sample:
                    break
        except Exception:
            print()
            print(logger.ERROR(f"article. ID = {id}"))
            print_error()

    if proccess_bar is False:
        logger.INFO("End export.")
    return output_list
