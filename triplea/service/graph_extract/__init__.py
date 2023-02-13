
import json
from triplea.schemas.article import Article
from triplea.schemas.node import Edge, Node
from triplea.service.export import export_graphml, generate_networkX
from triplea.service.ganalysis import sorted_degree_centrality, visualize_and_grouping
import triplea.service.ganalysis as anaz
from triplea.service.graph_extract.topic import _extract_article_topic
from triplea.service.persist import get_article_by_pmid, get_article_pmid_list_by_state


def Emmanuel(d:list)->list:
    """Base on [this](https://stackoverflow.com/questions/9427163/remove-duplicate-dict-in-list-in-python)

    Args:
        d (list): _description_

    Returns:
        list: _description_
    """
    return [i for n, i in enumerate(d) if i not in d[n + 1:]]



def thefourtheye_2(data):
    return {frozenset(item.items()):item for item in data}.values()

def graph_extractor(func):
    l_pmid = get_article_pmid_list_by_state(3)
    l_nodes=[]
    l_edges = []
    for id in l_pmid:
        a = get_article_by_pmid(id)
        try:
            article = Article(**a.copy())
        except:
            print('error')

        # data = _extract_article_topic(article)
        data = func(article)
        l_nodes.extend(data['nodes'])
        l_edges.extend(data['edges'])

        print(f'Nodes : {len(l_nodes)} Edges : {len(l_edges)}')

    print("----------------")
    n= Emmanuel(l_nodes)
    e =Emmanuel(l_edges)
    print(len(n))
    print(len(e))
    return { 'nodes' : l_nodes, 'edges' : l_edges}


def check_upper_term(n:dict,text:str):

    if n['Name'].__contains__(text.lower()):
        new_node = {'Name' : text.upper() , 'Type' : 'UpperTopic' , 'Identifier' : text.upper()}
        new_edge = {'SourceID' : n['Identifier'] ,
                        'DestinationID' : new_node['Identifier'],
                        'Type' : 'IS_A',
                        'HashID' : str(hash(n['Identifier'] + new_node['Identifier'] + 'IS_A'))
                        } 

        return {'node' : new_node , 'edge' : new_edge} 
    else:
        return None     


if __name__ == '__main__':
    # data = graph_extractor(_extract_article_topic)
    # data= json.dumps(data, indent=4)
    # with open("one-graph.json", "w") as outfile:
    #     outfile.write(data)
    # G = generate_networkX(data['nodes'],data['edges'])
    # export_graphml('topic',G)
    # visualize_and_grouping(G)

    # f = open('one-graph.json')
    # data = json.load(f)
    # f.close()

    # G = generate_networkX(data['nodes'],data['edges'])
    # export_graphml('topic1',G)
    # # visualize_and_grouping(G)

    # print(sorted_degree_centrality(G))
    # # print(anaz.sorted_betweenness_centrality(G))
    # anaz.info(G)


    f = open('one-graph.json')
    data = json.load(f)
    f.close()
    new_nodes =[]
    new_edges = []
    for n in data['nodes']:
        if n['Type'] == 'Topic':
            uv = check_upper_term(n,'cancer')
            if uv is not None:
                new_nodes.append(uv['node'])
                new_edges.append(uv['edge'])

            uv = check_upper_term(n,'breast')
            if uv is not None:
                new_nodes.append(uv['node'])
                new_edges.append(uv['edge'])

            uv = check_upper_term(n,'registry')
            if uv is not None:
                new_nodes.append(uv['node'])
                new_edges.append(uv['edge'])

            uv = check_upper_term(n,'data')
            if uv is not None:
                new_nodes.append(uv['node'])
                new_edges.append(uv['edge'])
                
    n= Emmanuel(new_nodes)
    e= Emmanuel(new_edges)
    data['nodes'].extend(n)
    data['edges'].extend(e)
    
    G = generate_networkX(data['nodes'],data['edges'])
    export_graphml('topic2',G)
    # visualize_and_grouping(G)
    print(sorted_degree_centrality(G))
    # print(anaz.sorted_betweenness_centrality(G))
    anaz.info(G)