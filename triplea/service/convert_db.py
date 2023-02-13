# from triplea.config.settings import SETTINGS,DB_ROOT_PATH
from triplea.db.mongodb import DB_MongoDB
from triplea.db.tinydb import DB_TinyDB
from triplea.schemas.article import Article
from triplea.service.click_logger import logger

from py2neo import Graph
from py2neo import Node,Relationship


from triplea.service.general import _extract_knowledge
from triplea.service.persist import get_article_by_pmid, get_article_pmid_list_by_state

def convert_to_neo4j():
    graph = Graph("bolt://neo4j:ehsan006@172.18.244.140:7687")
    l_pmid = get_article_pmid_list_by_state(4)
    total_node = []
    total_edge = []
    n = 10
    for id in l_pmid:
        a = get_article_by_pmid(id)
        article = Article(**a.copy())
        try:
            g = _extract_knowledge(article)
        except:
            nodes= []
            edges = []
            pass
        
        print(f'node : {len(total_node)} , edges : {len(total_edge)}' )


        total_node.extend (g['nodes'])
        total_edge.extend (g['edges'])
        

    print(len(total_node))
    print(len(total_edge))
        


def convert():
    source_db = DB_TinyDB()
    article_count = source_db.get_all_article_count()
    if article_count> 10000:
        pass
        # raise NotImplementedError

    la = source_db.get_article_by_state(0)
    destination_db = DB_MongoDB()
    n = 0  
    for a in la:
        pmid = a['PMID']
        if destination_db.is_article_exist_by_pmid(pmid):
            logger.INFO(f'The article {pmid} already exists.', deep = 3 )
        else:
            n = n +1
            destination_db.add_new_article(a)
            logger.DEBUG(f'{n} Copy article {pmid} to destination repository.', deep = 3 )

if __name__ == '__main__':
    # convert()
    convert_to_neo4j()

    # destination_db = DB_MongoDB()  
    # print(destination_db.get_all_article_count())
    # la = destination_db.get_article_by_state(3)
    # for a in la:
    #     print(a)

    # a = destination_db.get_article_by_pmid('36715845')
    # a = destination_db.is_article_exist_by_pmid('36715845')
    # print(type(a))
    # print(a)
    # destination_db.col_article.drop()
    



