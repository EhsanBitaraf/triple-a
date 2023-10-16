import sys
import traceback
from typing import Optional
import click
from triplea.config.settings import SETTINGS
from triplea.service.click_logger import logger
from triplea.schemas.article import Article
import triplea.service.repository.state as state_manager
import triplea.service.repository.persist as persist

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

            elif current_state == 2:  # Net state: Get Citation
                updated_article = state_manager.get_citation(updated_article)

            elif current_state == 3:  # Net state: NER Title
                updated_article = state_manager.ner_title(updated_article)

            elif persist.current_state == 4:  # Net state:Create Knowledge
                pass

            else:
                raise NotImplementedError

        persist.update_article_by_pmid(updated_article, updated_article.PMID)
        bar.label = (
            "Article "
            + updated_article.PMID
            + " with state "
            + str(updated_article_current_state)
            + " forward to "
            + str(end_state)
        )
        bar.update(1)
    persist.refresh()


def move_state_forward(
    state: int,
    tps_limit: Optional[int] = 1,
    extend_by_refrence: Optional[bool] = False,
    extend_by_cited: Optional[bool] = False,
):
    """
    It takes an article, extracts the data from it, and then creates a node and edge for each author and
    affiliation

    :param state: The state of the article in Knowledge Repository you want to move forward
    :type state: int
    :param tps_limit: The number of requests per second you want to make to the API, defaults to 1
    :type tps_limit: Optional[int] (optional)
    """

    # la = get_article_by_state(state) # old version
    l_pmid = persist.get_article_pmid_list_by_state(state)
    total_article_in_current_state = len(l_pmid)
    number_of_article_move_forward = 0
    logger.DEBUG(str(len(l_pmid)) + " Article(s) is in state " + str(state))

    bar = click.progressbar(length=len(l_pmid), show_pos=True, show_percent=True)

    refresh_point = 0
    for id in l_pmid:
        try:
            number_of_article_move_forward = number_of_article_move_forward + 1
            current_state = None

            if refresh_point == 500:
                refresh_point = 0
                persist.refresh()
                print()
                logger.INFO(
                    f"There are {str(total_article_in_current_state - number_of_article_move_forward)} article(s) left ",
                    forecolore="yellow",
                )
                # min = (
                #     total_article_in_current_state - number_of_article_move_forward
                # ) / 60
                # logger.INFO(
                #     f"It takes at least {str(int(min))} minutes or {str(int(min/60))} hours",
                #     forecolore="yellow",
                # )
            else:
                refresh_point = refresh_point + 1

            a = persist.get_article_by_pmid(id)
            # a = persist.get_article_by_pmid('35970485') # CRITICAL For Test and Debug

            try:
                updated_article = Article(**a.copy())
            except Exception:
                # print()
                # backward_dict = a.copy()
                # backward = Article()
                # backward.PMID = backward_dict['PMID']
                # logger.ERROR(f'Error in parsing article. PMID = {backward.PMID}')
                # backward.State = 0
                # updated_article = backward
                # l = update_article_by_pmid(updated_article , updated_article.PMID)
                print()
                print(logger.ERROR(f"Error in parsing article. PMID = {id}"))
                raise Exception("Article Not Parsed.")

            try:
                current_state = updated_article.State
            except Exception:
                current_state = 0

            # logger.DEBUG('Article ' + updated_article.PMID + ' with state ' + str(current_state) + ' forward to ' + str(current_state + 1))
            bar.label = (
                "Article "
                + updated_article.PMID
                + " with state "
                + str(current_state)
                + " forward to "
                + str(current_state + 1)
            )
            bar.update(1)
            # # for re run
            # if current_state == 2 : current_state = 1

            if current_state is None:
                updated_article = state_manager.expand_details(updated_article)
                persist.update_article_by_pmid(updated_article, updated_article.PMID)

            elif current_state == -1:  # Error in State 0 Net state: 1
                updated_article = state_manager.parsing_details(updated_article)
                persist.update_article_by_pmid(updated_article, updated_article.PMID)

            elif current_state == 0:  # Net state: get article details from pubmed
                updated_article = state_manager.expand_details(updated_article)
                persist.update_article_by_pmid(updated_article, updated_article.PMID)

            elif current_state == 1:  # Net state: Extract Data
                updated_article = state_manager.parsing_details(updated_article)
                persist.update_article_by_pmid(updated_article, updated_article.PMID)
                # # think after
                # if len(l) == 1:
                #     pass
                # else:
                #     logger.ERROR('Duplication has Occurred')

            elif current_state == 2:  # Net state: Get Citation
                updated_article = state_manager.get_citation(updated_article)
                persist.update_article_by_pmid(updated_article, updated_article.PMID)
                # think after
                # if len(l) == 1:
                #     pass
                # else:
                #     logger.ERROR('Duplication has Occurred')

            elif current_state == 3:  # Net state: NER Title
                updated_article = state_manager.ner_title(updated_article)
                persist.update_article_by_pmid(updated_article, updated_article.PMID)
                # think after
                # if len(l) == 1:
                #     pass
                # else:
                #     logger.ERROR('Duplication has Occurred')

        except Exception:
            if current_state == 1:
                updated_article = Article(**a.copy())
                updated_article.State = -1
                persist.update_article_by_pmid(updated_article, updated_article.PMID)
                persist.refresh()
                exc_type, exc_value, exc_tb = sys.exc_info()
                print()
                logger.ERROR(f"Error {exc_type}")
                logger.ERROR(f"Error {exc_value}")

            elif current_state is None:
                # Article Not Parsed.
                persist.refresh()
                exc_type, exc_value, exc_tb = sys.exc_info()
                print()
                logger.ERROR(f"Error {exc_type}")
                logger.ERROR(f"Error {exc_value}")

            elif current_state == 2:
                updated_article = Article(**a.copy())
                updated_article.State = -2
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


if __name__ == "__main__":
    logger.WARNING(
        "Number of article in knowlege repository is "
        + str(persist.get_all_article_count())
    )
    logger.WARNING(f"{persist.get_all_node_count()} Node(s) in knowlege repository.")
    logger.WARNING(f"{persist.get_all_edge_count()} Edge(s) in knowlege repository.")
    data = persist.get_article_group_by_state()
    for i in range(-3, 7):
        w = 0
        for s in data:
            if s["State"] == i:
                w = 1
                n = s["n"]
                logger.INFO(f"{n} article(s) in state {i}.")
        if w == 0:
            logger.INFO(f"0 article(s) in state {i}.")

    # s = '''("Breast Neoplasms"[Mesh] OR "Breast Cancer"[Title] OR
    #          "Breast Neoplasms"[Title] OR  "Breast Neoplasms"[Other Term] OR
    #          "Breast Cancer"[Other Term])
    #         AND
    #         ("Registries"[MeSH Major Topic] OR "Database Management Systems"[MeSH Major Topic] OR
    #          "Information Systems"[MeSH Major Topic] OR "Registry"[Other Term] OR "Registry"[Title] OR
    #          "Information Storage and Retrieval"[MeSH Major Topic])'''
    # get_article_list_all_store_to_kg_rep(s)

    # move_state_forward(3)
    # move_state_until(3)
    # refresh()

    # data = get_article_by_pmid('35130239')
    # data= json.dumps(data, indent=4)
    # with open("one-35130239.json", "w") as outfile:
    #     outfile.write(data)

    # 32434767
    # click.echo(click.style('Number of article in knowlege repository is ', fg='green') + ' ' + click.style(str(get_all_article_count()), fg='red'))
    # click.secho('Hello World!', fg='green')
    # click.secho('Some more text', bg='blue', fg='white')
    # click.secho('ATTENTION', blink=True, bold=True)

    # # Save Title for Annotation
    # file =  open("article-title.txt", "w",  encoding="utf-8")
    # la = get_article_by_state(2)
    # for a in la:
    #     try:
    #         article = Article(**a.copy())
    #     except:
    #         pass
    #     file.write(article.Title + "\n")

    # # Get list of cited article
    # data = get_cited_article_from_pubmed('26951748')
    # data = json.dumps(data, indent=4)
    # with open("one-cite.json", "w") as outfile:
    #     outfile.write(data)

    # print(insert_new_pmid('36619805',
    #                             reference_crawler_deep=SETTINGS.AAA_REFF_CRAWLER_DEEP,
    #                             cite_crawler_deep=SETTINGS.AAA_CITED_CRAWLER_DEEP))

    # refresh()
