from triplea.schemas.article import Article
from triplea.service.repository.export.unified_export_json.general import (
    _json_converter_author_general,
)


def _json_converter_01_arxiv(article: Article):
    title = article.Title
    publisher = article.Journal
    doi = article.DOI
    pmid = article.PMID
    state = article.State
    abstract = article.Abstract
    url = f"https://arxiv.org/abs/{article.ArxivID}/"
    journal_issn = "2331-8422"
    journal_iso_abbreviation = "ArXiv"
    year = article.Published.year
    publication_type = "Preprint"
    language = ""
    citation_count = None

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
