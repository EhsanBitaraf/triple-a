import click
from triplea.cli.main import cli
import triplea.service.graph.extract as gextract
import triplea.service.graph.export as gexport
import triplea.service.graph.analysis as ganalysis
from triplea.service.click_logger import logger


@cli.command("analysis", help="Analysis Graph.")
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

article-author-affiliation : It considers article, author and affiliation
 as nodes and edges between them

article-keyword : It considers article and keyword as nodes and
edges between them

article-reference : It considers article and reference as nodes and
edges between them

article-cited : It considers article and cited as nodes and edges between them

""",
)
@click.option(
    "--command",
    "-c",
    "command",
    type=click.Choice(["info", "sdc", "sdd"]),
    multiple=False,
    required=True,
    help="""Analysis Graph.
                    info :
                    sdc : sorted_degree_centrality
                    sdd : show_degree_distribution
                    """,
)
def analysis(generate_type, command):
    logger.INFO("Generate Graph ... ")
    l_nodes = []
    l_edges = []
    for g_type in generate_type:
        if g_type == "store":
            raise NotImplementedError
        elif g_type == "gen-all":
            graphdict = gextract.graph_extractor_all_entity()
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        elif g_type == "article-topic":
            graphdict = gextract.graph_extractor(gextract.graph_extract_article_topic)
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        elif g_type == "article-author-affiliation":
            graphdict = gextract.graph_extractor(
                gextract.graph_extract_article_author_affiliation
            )
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        elif g_type == "article-keyword":
            graphdict = gextract.graph_extractor(gextract.graph_extract_article_keyword)
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        elif g_type == "article-reference":
            graphdict = gextract.graph_extractor(
                gextract.graph_extract_article_reference
            )
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        elif g_type == "article-cited":
            graphdict = gextract.graph_extractor(gextract.graph_extract_article_cited)
            l_nodes.extend(graphdict["nodes"])
            l_edges.extend(graphdict["edges"])

        else:
            logger.ERROR(
                f"""Invalid value for
                          '--generate' / '-g': {generate_type}"""
            )

    print()
    # logger.DEBUG(f'Remove duplication in Nodes & Edges. ')
    n = gextract.Emmanuel(l_nodes)
    e = gextract.Emmanuel(l_edges)
    graphdict = {"nodes": n, "edges": e}

    if command == "info":
        G = gexport.export_networkx_from_graphdict(graphdict)
        ganalysis.info(G)
    elif command == "sdc":
        G = gexport.export_networkx_from_graphdict(graphdict)
        print(ganalysis.sorted_degree_centrality(G))
    elif command == "sdd":
        G = gexport.export_networkx_from_graphdict(graphdict)
        ganalysis.show_degree_distribution(G)
    else:
        logger.ERROR(f"Invalid value for '--command' / '-c': {command}")


if __name__ == "__main__":
    graphdict = gextract.graph_extractor(gextract.graph_extract_article_cited)
    l_nodes = []
    l_edges = []
    l_nodes.extend(graphdict["nodes"])
    l_edges.extend(graphdict["edges"])
    n = gextract.Emmanuel(l_nodes)
    e = gextract.Emmanuel(l_edges)
    graphdict = {"nodes": n, "edges": e}

    # import triplea.service.repository.persist as pr
    # d = pr.get_article_by_pmid('31398071')
    # print(d)
