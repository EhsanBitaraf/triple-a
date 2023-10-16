import click
# from py2neo import Graph
import triplea.service.graph.extract as gextract


def _replace_specific_char(text: str):
    """
    It replaces all the characters that are not allowed in Neo4j with a space

    :param text: The text to be cleaned
    :type text: str
    """

    text = text.replace('"', " ")
    text = text.replace("*", " ")
    text = text.replace("^", " ")
    text = text.replace("/", " ")
    text = text.replace("%", " ")
    text = text.replace(".", " ")

    # node labels, '[', "=~", IN, STARTS, ENDS, CONTAINS, IS, '^', '*', '/', '%', '+', '-', '=', '~', "<>", "!=", '<', '>', "<=", ">=", AND, XOR, OR, ',' or '}' (line 1, column 51 (offset: 50))

    return text


def export_to_neo4j(graphdict: dict, neoj4_bolt_url: str):
    """
    It takes a graph dictionary and a neo4j bolt url and exports the graph to neo4j

    :param graphdict: This is the dictionary that contains the nodes and edges
    :type graphdict: dict
    :param neoj4_bolt_url: The URL of your Neo4j instance
    :type neoj4_bolt_url: str
    """
    pass # Disable Because py2neo package lost.
    # graph = Graph(neoj4_bolt_url)
    # n = len(graphdict["nodes"]) + len(graphdict["edges"])
    # bar = click.progressbar(length=n, show_pos=True, show_percent=True)

    # for n in graphdict["nodes"]:
    #     name = _replace_specific_char(n["Name"])
    #     identifier = n["Identifier"]
    #     type = n["Type"]

    #     a = (
    #         "CREATE (n:"
    #         + type
    #         + '{Identifier: "'
    #         + name
    #         + '" , HashID: '
    #         + identifier
    #         + ' , Type: "'
    #         + type
    #         + '" })'
    #     )
    #     graph.run(a)
    #     bar.update(1)

    #     #  "bolt://neo4j:ehsan006@172.18.244.140:7687"

    #     # Get Node
    #     # MATCH (n{Identifier : 36715845}) RETURN n
    #     # Delete Node
    #     # MATCH (n {Identifier: -5324177750855482371}) DETACH DELETE n

    # for e in graphdict["edges"]:
    #     hashid = e["HashID"]
    #     src_id = e["SourceID"]
    #     des_id = e["DestinationID"]
    #     type = e["Type"]

    #     r = (
    #         """
    #         MATCH (a), (b) WHERE a.HashID = """
    #         + src_id
    #         + """ AND b.HashID = """
    #         + des_id
    #         + """
    #         CREATE (a)-[r:"""
    #         + type
    #         + """ {HashID: """
    #         + hashid
    #         + """}]->(b) RETURN a,b
    #         """
    #     )
    #     graph.run(r)
    #     bar.update(1)


if __name__ == "__main__":
    pass
    # graphdict = graph_extractor(graph_extract_article_author_affiliation, 2)

    # data= json.dumps(graphdict, indent=4)
    # with open("one-graphdict-author.json", "w") as outfile:
    #     outfile.write(data)

    # f = open('one-graphdict-author.json')
    # data = json.load(f)
    # f.close()

    # graphdict = graph_extractor(graph_extract_article_author_affiliation, state = 4 ,limit_node= 1000)
    graphdict = gextract.graph_extractor_all_entity(state=4, limit_node=9)
    export_to_neo4j(graphdict, "bolt://neo4j:ehsan006@172.18.244.140:7687")
