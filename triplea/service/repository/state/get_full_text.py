





from triplea.schemas.article import Article, SourceBankType

def _get_full_text_pubmed(article:Article):
    pass

def _get_full_text_arxiv(article:Article):
    pass

def get_full_text(article:Article):
    # Temporary Disable
    # # previous state is 3
    # article.State = 4  # next state
    # backward_state = -3

    if article.SourceBank is None:
        # This is Pubmed
        updated_article = _get_full_text_pubmed(article)
    elif article.SourceBank == SourceBankType.PUBMED:
        updated_article = _get_full_text_pubmed(article)
    elif article.SourceBank == SourceBankType.ARXIV:
        updated_article = _get_full_text_arxiv(article)
    else:
        raise NotImplementedError

    return updated_article