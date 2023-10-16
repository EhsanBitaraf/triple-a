import click
import sys
import os
from triplea.schemas.article import Article
import triplea.service.repository.persist as persist
from triplea.service.click_logger import logger


def export_pretrain_llm_in_dir(
    output_directory, Merge=True, proccess_bar=False, limit_sample=0, state=None
):
    """
    The function `export_pretrain_llm_in_dir` exports text data from articles in a
    given directory, either merging them into a single file or saving each article
    separately.

    :param output_directory: The directory where the exported files will be saved
    :param Merge: The `Merge` parameter determines whether to merge all the
    extracted text into a single file (`True`) or save each article's text in a
    separate file (`False`), defaults to True (optional)
    :param proccess_bar: The `proccess_bar` parameter is a boolean flag that
    determines whether or not to display a progress bar during the execution of the
    function. If set to `True`, a progress bar will be shown. If set to `False`, no
    progress bar will be displayed, defaults to False (optional)
    :param limit_sample: The `limit_sample` parameter is used to specify the
    maximum number of articles to process. If the value is set to 0, it means there
    is no limit and all articles will be processed, defaults to 0 (optional)
    :param state: The `state` parameter is used to filter the articles based on
    their state. If a value is provided for `state`, only articles with that
    specific state will be processed. If `state` is set to `None`, all articles
    will be processed
    """
    if state is None:
        l_pmid = persist.get_all_article_pmid_list()
        logger.INFO(f"{str(len(l_pmid))} Article(s) in Article Repository")
    else:
        l_pmid = persist.get_article_pmid_list_by_state(state)
        logger.INFO(
            f"{str(len(l_pmid))} Article(s) is in state {str(state)} in Article Repository"
        )

    n = 0
    if proccess_bar:
        bar = click.progressbar(length=len(l_pmid), show_pos=True, show_percent=True)

    # if os.path.exists(ROOT / path ):
    #     pass
    # else:
    #     os.mkdir(ROOT / path)

    if os.path.exists(output_directory):
        pass
    else:
        os.mkdir(output_directory)

    Merge_text_extract = ""

    for id in l_pmid:
        n = n + 1
        if proccess_bar:
            bar.update(1)
        a = persist.get_article_by_pmid(id)
        try:
            article = Article(**a.copy())
        except Exception:
            exc_type, exc_value, exc_tb = sys.exc_info()
            print()
            logger.ERROR(f"Error {exc_type}")
            logger.ERROR(f"Error {exc_value}")
            # logger.ERROR(f'Error {exc_tb.tb_next}')
            article = None

        if limit_sample != 0:  # Unlimited
            if n > limit_sample:
                break

        text_extract = ""
        a_title = ""
        a_abstract = ""
        if article is not None:
            if article.Title is not None:
                a_title = article.Title
            if article.Abstract is not None:
                a_abstract = article.Abstract

        text_extract = a_title + " " + a_abstract

        if Merge:
            Merge_text_extract = Merge_text_extract + text_extract
        else:  # Merge = false
            file_path = os.path.join(output_directory, f"{article.PMID}.txt")
            f = open(file_path, "w", encoding="utf-8")
            f.write(text_extract)
            f.close()
            if proccess_bar:
                bar.label = f"Article ({n}) (PMID : {article.PMID}): Saved."

    if Merge:
        file_path = os.path.join(output_directory, "pretrain_llm.txt")
        f = open(file_path, "w", encoding="utf-8")
        f.write(Merge_text_extract)
        f.close()

    print()
    logger.INFO("Task Done.")
