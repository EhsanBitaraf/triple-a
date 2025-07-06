from triplea.schemas.article import Article
from triplea.service.repository.export.unified_export_json.general import (
    _json_converter_author_general,
)


def _json_converter_01_wos(article: Article):
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
    if isinstance(article.OreginalArticle, dict):
        for i in article.OreginalArticle["file"]:
            tag = i[0:2]
            if tag == "DO":
                url = "https://doi.org/" + str.replace(i[6: len(i)], "\n", "")
            elif tag == "LA":
                language = str.replace(i[6: len(i)], "\n", "")
            elif tag == "PY":
                year = str.replace(i[6: len(i)], "\n", "")
            elif tag == "TY":
                publication_type = str.replace(i[6: len(i)], "\n", "")
            elif tag == "SN":
                ji = str.replace(i[6: len(i)], "\n", "")
                if len(ji) == 9 and not (ji.__contains__("X")):
                    journal_issn = ji

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
