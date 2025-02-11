from triplea.schemas.article import Article, SourceBankType
from triplea.service.repository.export.unified_export_json.arxiv import (
    _json_converter_01_arxiv,
)
from triplea.service.repository.export.unified_export_json.pubmed import (
    _json_converter_01_pubmed,
)
from triplea.service.repository.export.unified_export_json.scopus import _json_converter_01_scopus
from triplea.service.repository.export.unified_export_json.wos import _json_converter_01_wos

# from triplea.service.graph.extract import Emmanuel

def Emmanuel(d: list) -> list:
    """Base on [this](https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python)

    Args:
        d (list): _description_

    Returns:
        list: _description_
    """
    return [i for n, i in enumerate(d) if i not in d[n + 1 :]]

def json_converter_01(article: Article):
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
        json_article = _json_converter_01_scopus(article) # I dont know
    elif article.SourceBank == SourceBankType.GOOGLESCHOLAR:
        json_article = _json_converter_01_scopus(article) # I dont know
    else:
        raise NotImplementedError

    return json_article


def json_converter_02(article: Article):
    # In this conversion we make uniform AffiliationIntegration , 
    # citation_count in WOS and Author
    # add source

    c1 = json_converter_01(article)
    c1['source'] = article.SourceBank 

    author_fullname_list = []

        # Check SourceBank
    if article.SourceBank is None:
        # This is Pubmed
        article.SourceBank = SourceBankType.PUBMED
        c1['source'] = SourceBankType.PUBMED
        
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
        c1['authors'] = author_fullname_list

    elif article.SourceBank == SourceBankType.ARXIV:
        pass
        # json_article = _json_converter_01_arxiv(article)
    elif article.SourceBank == SourceBankType.WOS:
        if article.InsertType[0] == "From RIS":
            for tag in article.OreginalArticle['file']:
                if tag.__contains__("N1  - Times Cited in Web of Science Core Collection:"):
                    t = tag.replace("N1  - Times Cited in Web of Science Core Collection:", "")
                    t = t.replace("\n", "")
                    t = int(t)
                    c1['citation_count'] = t
        for author in article.Authors:
            author_fullname_list.append(author.FullName)
        c1['authors'] = author_fullname_list

    elif article.SourceBank == SourceBankType.SCOPUS:
        pass
        # json_article = _json_converter_01_scopus(article)
    elif article.SourceBank == SourceBankType.IEEE:
        pass
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
            if 'Structural' in ai:
                for i in ai['Structural']:
                    if 'country' in i: 
                        aic.append(i['country'])
                    if 'department' in i:
                        aid.append(i['department'])
                    if 'institution' in i:
                        aii.append(i['institution'])
        c1['affiliation_integration_country'] = Emmanuel(aic)
        c1['affiliation_integration_department'] = Emmanuel(aid)
        c1['affiliation_integration_institution'] = Emmanuel(aii)



    return c1