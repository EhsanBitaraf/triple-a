from triplea.schemas.article import Article
from triplea.service.repository.export.unified_export_json.general import (
    _json_converter_author_general,
)


def _json_converter_01_pubmed(article: Article):
    title = ""
    year = ""
    publisher = ""
    journal_issn = ""
    journal_iso_abbreviation = ""
    language = ""
    publication_type = ""

    title = article.Title
    publisher = article.Journal
    doi = article.DOI
    pmid = article.PMID
    state = article.State
    url = f"https://pubmed.ncbi.nlm.nih.gov/{article.PMID}/"

    # ------------------------year--------------------------------
    try:
        year = article.OreginalArticle["PubmedArticleSet"]["PubmedArticle"][
            "MedlineCitation"
        ]["Article"]["Journal"]["JournalIssue"]["PubDate"]["Year"]
    except Exception:
        try:
            year = article.OreginalArticle["PubmedArticleSet"]["PubmedArticle"][
                "MedlineCitation"
            ]["Article"]["Journal"]["JournalIssue"]["PubDate"]["MedlineDate"]
        except Exception:
            year = "0"
            # with open("sample.json", "w") as outfile:
            #     json.dump(article.OreginalArticle, outfile)
    # ------------------------year--------------------------------

    # ------------------------ISSN--------------------------------
    try:
        journal_issn = article.OreginalArticle["PubmedArticleSet"]["PubmedArticle"][
            "MedlineCitation"
        ]["Article"]["Journal"]["ISSN"]["#text"]
    except Exception:
        journal_issn = ""
    # ------------------------ISSN--------------------------------

    # ------------------------Journal ISO abv---------------------
    journal_iso_abbreviation = article.OreginalArticle["PubmedArticleSet"][
        "PubmedArticle"
    ]["MedlineCitation"]["Article"]["Journal"]["ISOAbbreviation"]
    journal_iso_abbreviation = journal_iso_abbreviation
    # ------------------------Journal ISO abv---------------------

    # ------------------------Language----------------------------
    lang = article.OreginalArticle["PubmedArticleSet"]["PubmedArticle"][
        "MedlineCitation"
    ]["Article"]["Language"]
    if isinstance(lang, list):
        for lg in lang:
            language = lg + ", " + language
        language = language[:-1]
    else:
        language = lang
    language = language
    # ------------------------Language----------------------------

    # ------------------------Publication Type--------------------
    p = article.OreginalArticle["PubmedArticleSet"]["PubmedArticle"]["MedlineCitation"][
        "Article"
    ]["PublicationTypeList"]["PublicationType"]
    if isinstance(p, list):
        for i in p:
            chunk = i["#text"]
            publication_type = chunk + ", " + publication_type
        # publication_type = p[0]['#text']
        publication_type = publication_type[:-1]
    else:
        publication_type = article.OreginalArticle["PubmedArticleSet"]["PubmedArticle"][
            "MedlineCitation"
        ]["Article"]["PublicationTypeList"]["PublicationType"]["#text"]
    publication_type = publication_type
    # ------------------------Publication Type--------------------

    # ------------------------Abstract----------------------------
    if article.Abstract is None:
        abstract = ""
    else:
        if article.Abstract.__contains__(","):
            abstract = article.Abstract.replace('"', " ")
            abstract = f'"{abstract}"'
        else:
            abstract = article.Abstract
    # ------------------------Abstract----------------------------

    # ------------------------Citation Count-----------------------
    citation_count = 0
    if article.CitedBy is not None:
        citation_count = len(article.CitedBy)
    # ------------------------Citation Count-----------------------

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
