import json
import sys
import click
from triplea.cli.main import cli
import triplea.service.graph.extract as gextract
import triplea.service.graph.export as gexport
from triplea.service.click_logger import logger


"""
Export Graph.

This function is used as a command in a command-line interface (CLI) tool.
 It generates a graph based on the specified type and exports
 it to the specified format. The exported graph is saved in
   the specified output file.

Parameters:
- generate_type (str): The type of graph to generate.
 It can take multiple values from a predefined list.
- format_type (str): The format in which the graph should be exported.
 It can take a single value from a predefined list.
- output_file (str): The file name and path of the output graph format.
- proccess_bar (bool, optional):
Whether to display a progress bar during graph generation. Defaults to True.
- remove_duplicate (bool, optional):
Whether to remove duplicate nodes and edges from the graph. Defaults to True.

Returns:
None

Example Usage:
$ python my_tool.py export_graph --generate article-topic
--format graphdict --output output.json

Note:
- The `generate_type` parameter can take the following values:
    - "store":
    Considers all the nodes and edges that are stored in the database.
    - "gen-all":
    Considers all possible nodes and edges.
    - "article-topic":
    Considers article and topic as nodes and edges between them.
    - "article-
    author-affiliation": Considers article, author,
    and affiliation as nodes and edges between them.
    - "article-keyword":
    Considers article and keyword as nodes and edges between them.
    - "article-reference":
    Considers article and reference as nodes and edges between them.
    - "article-cited":
    Considers article and cited as nodes and edges between them.
    - "country-authorship":
    Considers country and authorship as nodes and edges between them.

- The `format_type` parameter can take the following values:
    - "graphdict":
    A customized format for citation graphs in the form of a Python dictionary.
    - "graphjson":
    - "gson":
    - "gpickle": Writes the graph in Python pickle format.
    - "graphml":
    The GraphML file format uses .graphml extension and is XML structured.
    - "gexf":
    GEXF (Graph Exchange XML Format) is an XML-based file format
    for storing a single undirected or directed graph.
"""


@cli.command("export_graph", help="Export Graph.")
@click.option(
    "--generate",
    "-g",
    "generate_type",
    type=click.Choice(
        [
            "store",
            "gen-all",
            "article-topic",
            "article-author-affiliation",
            "article-keyword",
            "article-reference",
            "article-cited",
            "country-authorship",
        ]
    ),
    multiple=True,
    required=True,
    help="""Generate graph and export it.
    The type of graph construction can be different. These include:

    store : It considers all the nodes and edges
    that are stored in the database

    gen-all : It considers all possible nodes and edges

    article-topic : It considers article and topic
    as nodes and edges between them

    article-author-affiliation : It considers article, author
    and affiliation as nodes and edges between them

    article-keyword : It considers article and keyword
    as nodes and edges between them

    article-reference : It considers article and reference
    as nodes and edges between them

    article-cited : It considers article and cited
    as nodes and edges between them

    country-authorship :

                                """,
)
@click.option(
    "--format",
    "-f",
    "format_type",
    type=click.Choice(["graphdict", "graphjson", "gson", "gpickle", "graphml", "gexf"]),
    multiple=False,
    required=True,
    help="""Generate graph and export.
    graphdict : This format is a customized format for citation graphs
      in the form of a Python dictionary.

    graphjson :

    gson :

    gpickle : Write graph in Python pickle format.
      Pickles are a serialized byte stream of a Python object

    graphml : The GraphML file format uses .graphml extension
    and is XML structured. It supports attributes for nodes and edges,
      hierarchical graphs and benefits from a flexible architecture.

    gexf : GEXF (Graph Exchange XML Format) is an XML-based file format
      for storing a single undirected or directed graph.

                                """,
)
@click.option(
    "--output",
    "-o",
    "output_file",
    #   type=click.File('wb') ,
    type=str,
    multiple=False,
    required=True,
    help="File name & path of output graph format.",
)
@click.option(
    "--bar",
    "-b",
    "proccess_bar",
    type=bool,
    multiple=False,
    required=False,
    default=True,
    help="File name & path of output graph format.",
)
@click.option(
    "--removed",
    "-rd",
    "remove_duplicate",
    type=bool,
    multiple=False,
    required=False,
    default=True,
    help="File name & path of output graph format.",
)
def export_graph(
    generate_type, format_type, output_file, proccess_bar, remove_duplicate
):
    l_nodes = []
    l_edges = []
    for g_type in generate_type:
        if g_type == "store":
            raise NotImplementedError
        elif g_type == "gen-all":
            graphdict = gextract.graph_extractor_all_entity(
                remove_duplicate=remove_duplicate
            )
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        elif g_type == "article-topic":
            graphdict = gextract.graph_extractor(
                gextract.graph_extract_article_topic,
                proccess_bar=proccess_bar,
                remove_duplicate=remove_duplicate,
            )
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        elif g_type == "article-author-affiliation":
            graphdict = gextract.graph_extractor(
                gextract.graph_extract_article_author_affiliation,
                proccess_bar=proccess_bar,
                remove_duplicate=remove_duplicate,
            )
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        elif g_type == "article-keyword":
            graphdict = gextract.graph_extractor(
                gextract.graph_extract_article_keyword,
                proccess_bar=proccess_bar,
                remove_duplicate=remove_duplicate,
            )
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        elif g_type == "article-reference":
            graphdict = gextract.graph_extractor(
                gextract.graph_extract_article_reference,
                proccess_bar=proccess_bar,
                remove_duplicate=remove_duplicate,
            )
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        elif g_type == "article-cited":
            graphdict = gextract.graph_extractor(
                gextract.graph_extract_article_cited,
                proccess_bar=proccess_bar,
                remove_duplicate=remove_duplicate,
            )
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        elif g_type == "country-authorship":
            graphdict = gextract.graph_extractor(
                gextract.graph_extract_article_country,
                proccess_bar=proccess_bar,
                remove_duplicate=remove_duplicate,
            )
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        else:
            logger.ERROR(
                f"""Invalid value for
                          '--generate' / '-g': {generate_type}"""
            )
            sys.exit(1)

    print()
    # for temp
    logger.DEBUG("Save temp file with duplication.")
    data = json.dumps({"nodes": l_nodes, "edges": l_edges}, indent=4)
    with open("temp-with-duplication.json", "w") as outfile:
        outfile.write(data)
        outfile.close()
    if remove_duplicate:
        logger.DEBUG("Remove duplication in Nodes & Edges. ")
        n = gextract.thefourtheye_2(l_nodes)
        e = gextract.thefourtheye_2(l_edges)
        n = list(n)
        e = list(e)
        graphdict = {"nodes": n, "edges": e}
    else:
        graphdict = {"nodes": l_nodes, "edges": l_edges}

    if format_type == "graphdict":
        data1 = json.dumps(graphdict, indent=4)
        with open(output_file, "w") as outfile:
            outfile.write(data1)
    elif format_type == "graphjson":
        data = gexport.export_graphjson_from_graphdict(graphdict)
        data = json.dumps(data, indent=4)
        with open(output_file, "w") as outfile:
            outfile.write(data)
            outfile.close()
    elif format_type == "gson":
        data = gexport.export_gson_from_graphdict(graphdict)
        data = json.dumps(data, indent=4)
        with open(output_file, "w") as outfile:
            outfile.write(data)
            outfile.close()
    elif format_type == "gpickle":
        gexport.export_gpickle_from_graphdict(graphdict, output_file)
    elif format_type == "graphml":
        gexport.export_graphml_from_graphdict(graphdict, output_file)
    elif format_type == "gexf":
        gexport.export_gexf_from_graphdict(graphdict, output_file)
    else:
        logger.ERROR(f"Invalid value for '--format' / '-f': {format_type}")
        sys.exit(1)

    sys.exit(0)
