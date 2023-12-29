
from triplea.schemas.article import Article, SourceBankType
from triplea.service.repository.state import (parsing_details_arxiv,
                                              parsing_details_pubmed)


def parsing_details(article: Article) -> Article:
    # this is dispatcher function
    if article.SourceBank is None:
        # This is Pubmed
        updated_article = parsing_details_pubmed(article)
    elif article.SourceBank == SourceBankType.PUBMED:
        updated_article = parsing_details_pubmed(article)
    elif article.SourceBank == SourceBankType.ARXIV:
        updated_article = parsing_details_arxiv(article)
    else:
        raise NotImplementedError
    
    return updated_article