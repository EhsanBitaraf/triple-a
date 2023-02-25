

import json
from triplea.config.settings import ROOT
from triplea.service.graph.export.export import export_graphjson_from_graphdict, export_gson_from_graphdict


def refresh_interactivegraph(graphdict):
    """
    It takes a graph dictionary and exports it to a JSON file
    
    :param graphdict: a dictionary of the form {'nodes':[], 'edges':[]}
    """
    data = export_gson_from_graphdict(graphdict)

    data= json.dumps(data, indent=4)
    with open(ROOT.parent / 'visualization' / 'interactivegraph' / 'one-gson.json', "w") as outfile:
        outfile.write(data)

def refresh_alchemy(graphdict):
    """
    It takes a graph dictionary and exports it to a JSON file that can be read by the Alchemy.js library
    
    :param graphdict: a dictionary of dictionaries, where the keys are the nodes and the values are
    dictionaries of the node's attributes
    """
    data = export_graphjson_from_graphdict(graphdict)
    data= json.dumps(data, indent=4)
    with open(ROOT.parent / 'visualization' / 'alchemy' / 'data.json', "w") as outfile:
        outfile.write(data)