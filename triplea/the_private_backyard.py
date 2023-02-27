

import time
import networkx as nx
# import nxviz as nv??
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from netwulf import visualize

import json
from triplea.service.graph import extract

import  triplea.service.graph.analysis.ganalysis as ganaliz
import triplea.service.graph.export.export as gexport
import triplea.service.graph.extract as gextract
# import triplea.service.graph.export as gexport
from triplea.service.graph.extract import Emmanuel, check_upper_term , _t_emmanuel
from triplea.service.click_logger import logger

def check_map_topic():
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

    G = gexport.export_networkx_from_graphdict(data)
    ganaliz.info(G)

if __name__ == '__main__':

    # graphdict = extract.graph_extractor(gextract.graph_extract_article_keyword, limit_node= 2000 )
    # G = gexport.export_networkx_from_graphdict(graphdict,graph_type='undirected')



    f = open('temp.json')
    data = json.load(f)
    f.close() 

    G = gexport.export_networkx_from_graphdict(data,graph_type='directed')
    ganaliz.info(G)

    # n = extract._emmanuel(data['nodes'])
    # e = extract._emmanuel(data['edges']) 
    # start_time = time.time()
    # e =  extract.thefourtheye_2(data['edges'])
    # process_time = time.time() - start_time
    # logger.INFO(f'process_time : {str(process_time)}')

    # G1 = nx.k_core(G)
    # visualize(G1)
    # # nx.draw(G1)
    # # plt.show()


    # logger.INFO(f'Drawing ...')
    # nx.draw(G,
    #         pos=nx.spiral_layout(G),
    #         arrows=True,
    #         arrowstyle = 'Fancy',
    #         arrowsize= 1,
    #         with_labels = True,
    #         node_size = 30,
    #         node_color = '#ff5733',
    #         width = 2 ,
    #         edge_color = '#77ff33',
    #         font_size = 8)
    # plt.show()
    # plt.savefig("filename.png")


    # simple
    # graphdict = extract.graph_extractor_all_entity(state = 4 ,limit_node= 0)
    # data= json.dumps(graphdict, indent=4)
    # with open("one-graphdict-all.json", "w") as outfile:
    #     outfile.write(data)