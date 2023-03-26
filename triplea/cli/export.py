import json
import click
from triplea.cli.main import cli
import triplea.service.graph.extract as gextract
import triplea.service.graph.export as gexport
from triplea.service.click_logger import logger


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
        ]
    ),
    multiple=True,
    required=True,
    help="""Generate graph and export it.
                                The type of graph construction can be different. These include:

                                store : It considers all the nodes and edges that are stored in the database

                                gen-all : It considers all possible nodes and edges

                               article-topic : It considers article and topic as nodes and edges between them

                                article-author-affiliation : It considers article, author and affiliation as nodes and edges between them

                                article-keyword : It considers article and keyword as nodes and edges between them

                                article-reference : It considers article and reference as nodes and edges between them

                                article-cited : It considers article and cited as nodes and edges between them

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
                                graphdict : This format is a customized format for citation graphs in the form of a Python dictionary.

                                graphjson :

                                gson :

                                gpickle : Write graph in Python pickle format. Pickles are a serialized byte stream of a Python object

                                graphml : The GraphML file format uses .graphml extension and is XML structured. It supports attributes for nodes and edges, hierarchical graphs and benefits from a flexible architecture.

                                gexf : GEXF (Graph Exchange XML Format) is an XML-based file format for storing a single undirected or directed graph.

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
def export(generate_type, format_type, output_file, proccess_bar,remove_duplicate):
    l_nodes = []
    l_edges = []
    for g_type in generate_type:
        if g_type == "store":
            raise NotImplementedError
        elif g_type == "gen-all":
            graphdict = gextract.graph_extractor_all_entity(remove_duplicate=remove_duplicate)
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        elif g_type == "article-topic":
            graphdict = gextract.graph_extractor(gextract.graph_extract_article_topic,proccess_bar =proccess_bar,remove_duplicate=remove_duplicate)
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        elif g_type == "article-author-affiliation":
            graphdict = gextract.graph_extractor(
                gextract.graph_extract_article_author_affiliation,proccess_bar =proccess_bar,remove_duplicate=remove_duplicate
            )
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        elif g_type == "article-keyword":
            graphdict = gextract.graph_extractor(gextract.graph_extract_article_keyword,proccess_bar =proccess_bar,remove_duplicate=remove_duplicate)
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        elif g_type == "article-reference":
            graphdict = gextract.graph_extractor(
                gextract.graph_extract_article_reference,proccess_bar =proccess_bar,remove_duplicate=remove_duplicate
            )
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        elif g_type == "article-cited":
            graphdict = gextract.graph_extractor(gextract.graph_extract_article_cited,proccess_bar =proccess_bar,remove_duplicate=remove_duplicate)
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        else:
            logger.ERROR(f"Invalid value for '--generate' / '-g': {generate_type}")

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
