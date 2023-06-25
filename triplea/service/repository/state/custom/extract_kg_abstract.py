import sys
from triplea.schemas.article import Article
from triplea.service.click_logger import logger
from triplea.service.nlp.triple_extract import extract_triples
import triplea.service.repository.persist as persist

def extract_triple_abstract_save(article: Article):
    article.FlagExtractKG = 1
    if article.Abstract is not None:
        triples_list = extract_triples(article.Abstract)

        for t in triples_list:
            t['PMID'] = article.PMID
            persist.create_triple(t)

    return article


    
    

