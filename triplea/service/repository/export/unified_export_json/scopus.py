from triplea.schemas.article import Article
from triplea.service.repository.export.unified_export_json.general import (
    _json_converter_author_general,
)


def get_string_between(text: str, string1: str, string2: str):
    """
    This function returns the string between string1 and string2.
    """
    start = text.find(string1)
    if start != -1:
        end = text.find(string2, start + len(string1))
        if end != -1:
            return text[start + len(string1):end]
    return None


def _json_converter_01_scopus(article: Article):
    title = article.Title
    publisher = article.Journal
    doi = article.DOI
    pmid = ""
    state = article.State
    abstract = article.Abstract
    url = ""
    language = ""
    year = ""
    publication_type = ""
    journal_issn = ""
    journal_iso_abbreviation = ""
    citation_count = None
    if isinstance(article.OreginalArticle, dict):
        for i in article.OreginalArticle["file"]:
            tag = i[0:2]
            if tag == "UR":
                url = str.replace(i[6: len(i)], "\n", "")
            elif tag == "LA":
                language = str.replace(i[6: len(i)], "\n", "")
            elif tag == "PY":
                year = str.replace(i[6: len(i)], "\n", "")
            elif tag == "TY":
                publication_type = str.replace(i[6: len(i)], "\n", "")
            elif tag == "SN":
                ji = str.replace(i[6: len(i)], " (ISSN)\n", "")
                if len(ji) == 8:
                    journal_issn = f"{ji[0:4] }-{ji[4:8] }"
            # elif tag == "N1":
            #     citation = str.replace(i[6:len(i)],"\n" , "")
            #     citation_count = get_string_between(citation,"Cited By:",";")
            #     if citation_count is not None:
            #         citation_count = int(citation_count)

    citation_count = article.CitationCount  # in Update version 0.0.7

    # ------------------------Authors----------------------------
    list_authors = []
    if article.Authors is not None:
        for au in article.Authors:
            list_authors.append(_json_converter_author_general(au))
    # ------------------------Authors----------------------------

    r = {
        "title": title,
        "year": year,
        "publisher": publisher,
        "journal_issn": journal_issn,
        "journal_iso_abbreviation": journal_iso_abbreviation,
        "language": language,
        "publication_type": publication_type,
        "doi": doi,
        "pmid": pmid,
        "state": state,
        "url": url,
        "abstract": abstract,
        "citation_count": citation_count,
        "authors": list_authors,
        "keywords": article.Keywords,
        "topics": article.Topics,
    }
    return r
