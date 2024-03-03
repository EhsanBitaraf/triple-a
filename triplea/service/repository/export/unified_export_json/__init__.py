from triplea.schemas.article import Article, SourceBankType
from triplea.service.repository.export.unified_export_json.arxiv import (
    _json_converter_01_arxiv,
)
from triplea.service.repository.export.unified_export_json.pubmed import (
    _json_converter_01_pubmed,
)
from triplea.service.repository.export.unified_export_json.scopus import _json_converter_01_scopus
from triplea.service.repository.export.unified_export_json.wos import _json_converter_01_wos


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
    else:
        raise NotImplementedError

    return json_article
