from triplea.schemas.article import Article

# from triplea.service.nlp.triple_extract import extract_triples  # Expire Module
from triplea.client.triple_extraction import extract_triple
import triplea.service.repository.persist as persist


def extract_triple_abstract_save(article: Article, article_id):
    article.FlagExtractKG = 1
    if article.Abstract is not None:
        # triples_list = extract_triples(article.Abstract)  # Expire Module
        triples_list = []
        triples_list = extract_triple(article.Abstract)
        for t in triples_list:
            t["Article_ID"] = article_id
            persist.create_triple(t)

    return article
