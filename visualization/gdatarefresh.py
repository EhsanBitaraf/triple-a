

import json
from triplea.config.settings import ROOT
from triplea.service.graph.export.export import export_graphjson_from_graphdict, export_gson_from_graphdict


def refresh_interactivegraph(graphdict):
    data = export_gson_from_graphdict(graphdict)

    data= json.dumps(data, indent=4)
    with open(ROOT.parent / 'visualization' / 'interactivegraph' / 'one-gson.json', "w") as outfile:
        outfile.write(data)

def refresh_alchemy(graphdict):
    data = export_graphjson_from_graphdict(graphdict)
    data= json.dumps(data, indent=4)
    with open(ROOT.parent / 'visualization' / 'alchemy' / 'data.json', "w") as outfile:
        outfile.write(data)