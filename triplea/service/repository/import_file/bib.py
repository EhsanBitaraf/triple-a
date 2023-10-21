from triplea.service.click_logger import logger
from triplea.client.pubmed import get_article_list_from_pubmed
import triplea.service.repository.persist as persist
from triplea.service.repository.state.initial import _save_article_pmid_list_in_arepo


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
        # A BIB file is a text document
        # created by a LaTeX program,
        # such as MiKTeX or TeXworks.
        file_type = "bib"
    elif file_content.__contains__("%0 Journal Article"):
        # An .ENW file is an EndNote Export file.
        file_type = "enw"
    elif file_content.__contains__("TY  - JOUR"):
        # The RIS (file format) is a standardized tag format
        # developed by Research Information Systems company.
        # The tag includes two letters, two spaces,
        # and a hyphen to express bibliographic
        # citation information.
        file_type = "ris"
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
