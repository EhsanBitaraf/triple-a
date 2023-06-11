import time
from typing import Optional
from triplea.client.pubmed import get_article_list_from_pubmed
from triplea.service.click_logger import logger
from triplea.config.settings import SETTINGS
import triplea.service.repository.persist as persist


def _save_article_pmid_list_in_arepo(data: dict) -> None:
    """
    > If the data is in the right format, then for each PMID in the data, insert the PMID into the
    knowledge repository. If the PMID is not a duplicate, then log the PMID as added to the knowledge
    repository

    :param data: The output format from the pubmed service is for a list of PMIDs that is output from the `get_article_list_from_pubmed` method.
    :type data: dict
    """
    if "esearchresult" in data:
        qt = data["esearchresult"]["querytranslation"]
        n = 0
        for pmid in data["esearchresult"]["idlist"]:
            n = n + 1
            i = persist.insert_new_pmid(
                pmid,
                querytranslation=qt,
                reference_crawler_deep=SETTINGS.AAA_REFF_CRAWLER_DEEP,
                cite_crawler_deep=SETTINGS.AAA_CITED_CRAWLER_DEEP,
            )
            if i is None:  # PMID is Duplicate
                logger.INFO(f"{pmid} is exist in knowledge repository. ({n})")
            else:
                # logger.INFO('add ' + pmid + ' to knowledge repository. get ' + str(i))
                logger.INFO(f"add {pmid} to knowledge repository. ({n})")
    else:
        persist.refresh()
        logger.ERROR("data is not in right format.")
    persist.refresh()


# https://stackoverflow.com/questions/3368969/find-string-between-two-substrings
def _find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def _find_between_r(s, first, last):
    try:
        start = s.rindex(first) + len(first)
        end = s.rindex(last, start)
        return s[start:end]
    except ValueError:
        return ""


def get_article_from_bibliography_file_format(filepath: str):
    infile = open(filepath, "r")
    file_content = infile.read()
    infile.close()
    file_type = ""
    if file_content.__contains__("@article{"):
        file_type = "bib"  # A BIB file is a text document created by a LaTeX program, such as MiKTeX or TeXworks.
    elif file_content.__contains__("%0 Journal Article"):
        file_type = "enw"  # An .ENW file is an EndNote Export file.
    elif file_content.__contains__("TY  - JOUR"):
        file_type = "ris"  # The RIS (file format) is a standardized tag format developed by Research Information Systems company. The tag includes two letters, two spaces, and a hyphen to express bibliographic citation information.
    else:
        logger.ERROR("The file format is unknown to us.")
        return False
        # raise Exception('The file format is unknown to us.')

    if file_type == "bib":
        title = _find_between(file_content, "title={", "}")
    elif file_type == "enw":
        title = _find_between(file_content, "%T ", "\n")
    elif file_type == "ris":
        title = _find_between(file_content, "T1  - ", "\n")
    else:
        logger.ERROR("The file format is unknown to us.")
        return False
        # raise Exception('The file format is unknown to us.')
    searchterm = ""

    if title.lower().__contains__(" and "):
        t = title.lower().split(" and ")
        for i in t:
            searchterm = searchterm + i.strip() + "[Title] AND "
    elif title.lower().__contains__(" or "):
        t = title.lower().split(" and ")
        for i in t:
            searchterm = searchterm + i.strip() + "[Title] OR "
    else:
        searchterm = title.strip() + "[Title]"

    data = get_article_list_from_pubmed(0, 2, searchterm)
    total = int(data["esearchresult"]["count"])

    if total == 0:
        logger.WARNING("There is no article with this title in PubMed.")
        return False
    _save_article_pmid_list_in_arepo(data)
    persist.refresh()
    logger.INFO("The article was registered in Arepo.")

    return True


def get_article_list_from_pubmed_all_store_to_arepo(
    searchterm: str,
    tps_limit: Optional[int] = 1,
    big_ret: Optional[bool] = True,
    retmax: Optional[int] = 10000,
) -> None:
    """
    It takes a search term, and returns a list of all the articles that match that search term

    :param searchterm: The search term you want to use to search PubMed
    :type searchterm: str
    :param tps_limit: The number of requests per second, defaults to 1
    :type tps_limit: Optional[int] (optional)
    :param big_ret: If True, the function will return a maximum of 10,000 records. If False, it will
    return a maximum of 20 records, defaults to True
    :type big_ret: Optional[bool] (optional)
    :param retmax: The number of articles to return per request, defaults to 10000
    :type retmax: Optional[int] (optional)
    """
    sleep_time = 1 // tps_limit
    data = get_article_list_from_pubmed(0, 2, searchterm)

    total = int(data["esearchresult"]["count"])
    logger.INFO("Total number of article is " + str(total))

    if total == 0:
        return

    if big_ret:
        retmax = 10000
    else:
        retmax = 20

    if total >= retmax:
        round = total // retmax
    else:  # total < retmax
        retmax = total
        round = 2

    for i in range(1, round):
        time.sleep(sleep_time)
        logger.INFO(
            "Round ("
            + str(i)
            + ") : "
            + "Get another "
            + str(retmax)
            + " record (Total "
            + str(i * retmax)
            + " record)",
            deep=13,
        )
        start = (i * retmax) - retmax
        chunkdata = get_article_list_from_pubmed(start, retmax, searchterm)
        _save_article_pmid_list_in_arepo(chunkdata)

    # for last round
    start = ((i + 1) * retmax) - retmax
    mid = total - (retmax * round)
    logger.INFO(
        "Round ("
        + str(i + 1)
        + ") : "
        + "Get another "
        + str(mid)
        + " record (total "
        + str(total)
        + " record)",
        deep=13,
    )
    chunkdata = get_article_list_from_pubmed(start, retmax, searchterm)
    _save_article_pmid_list_in_arepo(chunkdata)


if __name__ == "__main__":
    pass
    # f = r"C:\Users\Bitaraf\Desktop\my-python-project\github\triple-a\tests\fixtures\cite-file\scholar.ris"
    # f = r"C:\Users\Dr bitaraf\Desktop\MyData\CodeRepo\github\triple-a\bc.ris"
    # print(get_article_from_bibliography_file_format(f))

    start = 1
    retmax = 10000
    searchterm = '"Biological Specimen Banks"[Mesh] OR BioBanking OR biobank OR dataBank OR "Bio Banking" OR "bio bank"'
    chunkdata = get_article_list_from_pubmed(start, retmax, searchterm)
    _save_article_pmid_list_in_arepo(chunkdata)
