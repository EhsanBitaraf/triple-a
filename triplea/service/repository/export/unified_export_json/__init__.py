from triplea.schemas.article import Article, SourceBankType
from triplea.service.repository.export.unified_export_json.arxiv import (
    _json_converter_01_arxiv,
)
from triplea.service.repository.export.unified_export_json.pubmed import (
    _json_converter_01_pubmed,
)
from triplea.service.repository.export.unified_export_json.scopus import (
    _json_converter_01_scopus,
)
from triplea.service.repository.export.unified_export_json.wos import (
    _json_converter_01_wos,
)

import warnings
from triplea.service.repository.export.unified_export_json.general import (
    _converter_authors_to_short, _json_converter_author_general)
# from triplea.service.graph.extract import Emmanuel


def Emmanuel(d: list) -> list:
    """Base on 
        [this](https://stackoverflow.com/questions/9427163/
        remove-duplicate-dict-in-list-in-python)

    Args:
        d (list): _description_

    Returns:
        list: _description_
    """
    return [i for n, i in enumerate(d) if i not in d[n + 1 :]]

def _json_converter_03(article: Article):
    # In this conversion after adding field to article -
    #  `Language`,`Year`, `SerialNumber` and `links`  
    title = article.Title
    publisher = article.Journal
    doi = article.DOI
    pmid = article.PMID
    state = article.State
    abstract = article.Abstract
    url = article.links
    language = article.Language
    year = article.Year
    publication_type = article.PublicationType
    journal_issn = article.SerialNumber
    journal_iso_abbreviation = ""
    citation_count = article.CitationCount


    # ------------------------Authors----------------------------
    
    list_authors = _converter_authors_to_short(article)
    # list_authors = []
    # if article.Authors is not None:
    #     for au in article.Authors:
    #         list_authors.append(_json_converter_author_general(au))
    # ------------------------Authors----------------------------

    # ------------------------Keywords----------------------------
    list_keywords = []
    if article.Keywords is not None:
        for k in article.Keywords:
            if k.IS_Mesh == True or k.IS_Mesh is None:
                list_keywords.append(k.Text)
    # ------------------------Keywords----------------------------

    # ------------------------Topics----------------------------
    list_topic = []
    if article.Topics is not None:
        for t in article.Topics:
            list_topic.append(t['text'])
    # ------------------------Topics----------------------------


    # ------------------------affiliation_integration--------------------------
    aic = []
    aid = []
    aii = []
    uni_list = []
    gov_list = []
    city_list = []
    aitext = []
    if article.AffiliationIntegration is not None:
        for ai in article.AffiliationIntegration:
            if "Structural" in ai:
                for i in ai["Structural"]:
                    if "country" in i:
                        aic.append(i["country"])
                    if "department" in i:
                        aid.append(i["department"])
                    if "institution" in i:
                        aii.append(i["institution"])

                    if "university" in i:
                        uni_list.append(i["university"])
                    if "government_entity" in i:
                        gov_list.append(i["government_entity"])
                    if "city" in i:
                        city_list.append(i["city"])
            if 'Text' in ai:
                aitext.append(ai['Text'])


    # ------------------------affiliation_integration--------------------------
    r = {
        "bank" : article.SourceBank,
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
        "keywords": list_keywords,
        "topics": list_topic,
        "affiliation_integration_country" :  Emmanuel(aic),
        "affiliation_integration_department" : Emmanuel(aid),
        "affiliation_integration_institution" : Emmanuel(aii),

        "affiliation_integration_university" :  Emmanuel(uni_list),
        "affiliation_integration_government_entity" : Emmanuel(gov_list),
        "affiliation_integration_city" : Emmanuel(city_list),

        "affiliation_integration_text" : Emmanuel(aitext)
    }
    return r


def json_converter_03(article: Article):
    return _json_converter_03(article)


## --------------------------------------deprecated-------------------------

def json_converter_01(article: Article):
    warnings.warn(
        """json_converter_01() is deprecated
          and will be removed in a future version.
          You can use json_converter_03""",
        DeprecationWarning,
        stacklevel=2
    )
    # Check SourceBank
    if article.SourceBank is None:
        # This is Pubmed
        json_article = _json_converter_01_pubmed(article)
    elif article.SourceBank == SourceBankType.PUBMED:
        json_article = _json_converter_01_pubmed(article)
    elif article.SourceBank == SourceBankType.ARXIV:
        json_article = _json_converter_01_arxiv(article)
    elif article.SourceBank == SourceBankType.WOS:
        json_article = _json_converter_01_wos(article)
    elif article.SourceBank == SourceBankType.SCOPUS:
        json_article = _json_converter_01_scopus(article)
    elif article.SourceBank == SourceBankType.IEEE:
        json_article = _json_converter_01_scopus(article)
    elif article.SourceBank == SourceBankType.UNKNOWN:
        json_article = _json_converter_01_scopus(article)  # I dont know
    elif article.SourceBank == SourceBankType.GOOGLESCHOLAR:
        json_article = _json_converter_01_scopus(article)  # I dont know
    elif article.SourceBank == SourceBankType.EMBASE:
        json_article = _json_converter_03(article)  # I dont know
    elif article.SourceBank == SourceBankType.ACM:
        json_article = _json_converter_03(article)  # I dont know
    else:
        raise NotImplementedError

    return json_article

def json_converter_02(article: Article):

    warnings.warn(
        """json_converter_01() is deprecated
          and will be removed in a future version.
          You can use json_converter_03""",
        DeprecationWarning,
        stacklevel=2
    )
    # In this conversion we make uniform AffiliationIntegration ,
    # citation_count in WOS and Author
    # add source



    c1 = json_converter_01(article)
    c1["source"] = article.SourceBank

    author_fullname_list = []

    # Check SourceBank
    if article.SourceBank is None:
        # This is Pubmed
        article.SourceBank = SourceBankType.PUBMED
        c1["source"] = SourceBankType.PUBMED

    elif article.SourceBank == SourceBankType.PUBMED:
        if article.Authors is None:
            pass
        else:
            for author in article.Authors:
                if author.ForeName is not None:
                    a = f"{author.LastName}, {author.ForeName[0:1]}"
                else:
                    a = author.FullName
                author_fullname_list.append(a)
        c1["authors"] = author_fullname_list

    elif article.SourceBank == SourceBankType.ARXIV:
        pass
        # json_article = _json_converter_01_arxiv(article)
    elif article.SourceBank == SourceBankType.WOS:
        if article.InsertType[0] == "From RIS":
            for tag in article.OreginalArticle["file"]:
                if tag.__contains__(
                    "N1  - Times Cited in Web of Science Core Collection:"
                ):
                    t = tag.replace(
                        "N1  - Times Cited in Web of Science Core Collection:", ""
                    )
                    t = t.replace("\n", "")
                    t = int(t)
                    c1["citation_count"] = t
        if article.Authors is not None:
            for author in article.Authors:
                author_fullname_list.append(author.FullName)
        c1["authors"] = author_fullname_list

    elif article.SourceBank == SourceBankType.SCOPUS:
        pass
        # json_article = _json_converter_01_scopus(article)
        if article.Authors is not None:
            for author in article.Authors:
                author_fullname_list.append(author.FullName)
        c1["authors"] = author_fullname_list

    elif article.SourceBank == SourceBankType.IEEE:
        pass
        if article.Authors is not None:
            for author in article.Authors:
                author_fullname_list.append(author.FullName)
        c1["authors"] = author_fullname_list
    elif article.SourceBank == SourceBankType.UNKNOWN:
        pass
    elif article.SourceBank == SourceBankType.GOOGLESCHOLAR:
        pass
    else:
        raise NotImplementedError

    aic = []
    aid = []
    aii = []
    if article.AffiliationIntegration is not None:
        for ai in article.AffiliationIntegration:
            if "Structural" in ai:
                for i in ai["Structural"]:
                    if "country" in i:
                        aic.append(i["country"])
                    if "department" in i:
                        aid.append(i["department"])
                    if "institution" in i:
                        aii.append(i["institution"])
        c1["affiliation_integration_country"] = Emmanuel(aic)
        c1["affiliation_integration_department"] = Emmanuel(aid)
        c1["affiliation_integration_institution"] = Emmanuel(aii)

    return c1
