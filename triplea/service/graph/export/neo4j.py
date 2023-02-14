
import json
from py2neo import Graph
from py2neo import Node,Relationship
from triplea.service.graph.extract import graph_extractor
from triplea.service.graph.extract import graph_extract_article_author_affiliation

def export_to_neo4j(graphdict:dict):
    graph = Graph("bolt://neo4j:ehsan006@172.18.244.140:7687")
    for n in graphdict['nodes']:
        neo_node = Node()
        Relationship(neo_node)

# def convert_to_neo4j():
#     graph = Graph("bolt://neo4j:ehsan006@172.18.244.140:7687")
#     l_pmid = get_article_pmid_list_by_state(4)
#     total_node = []
#     total_edge = []
#     n = 10
#     for id in l_pmid:
#         a = get_article_by_pmid(id)
#         article = Article(**a.copy())
#         try:
#             g = _extract_knowledge(article)
#         except:
#             nodes= []
#             edges = []
#             pass
        
#         print(f'node : {len(total_node)} , edges : {len(total_edge)}' )


#         total_node.extend (g['nodes'])
#         total_edge.extend (g['edges'])
        

#     print(len(total_node))
#     print(len(total_edge))
        
if __name__ == '__main__':
    pass
    # graphdict = graph_extractor(graph_extract_article_author_affiliation, 2)

    # data= json.dumps(graphdict, indent=4)
    # with open("one-graphdict-author.json", "w") as outfile:
    #     outfile.write(data)

    # f = open('one-graphdict-author.json')
    # data = json.load(f)
    # f.close()

    # export_to_neo4j(data)
    graph = Graph("bolt://neo4j:ehsan006@172.18.244.140:7687")
    neo_node = Node("test" , name = "testname")
    neo_node1 = Node("test1" , name = "testname1")
    rel = Relationship(neo_node,"IS_A",neo_node1)
    graph.create(neo_node)
    graph.create(neo_node1)
    graph.create(rel)

    print(rel[id])
