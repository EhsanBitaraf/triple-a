import networkx as nx
from networkx import is_directed
import time


def info(G, format="stdout"):
    start_time = time.time()
    graph_type = ""
    scc = ""
    wcc = ""
    reciprocity = ""
    diameter = ""
    num_components = ""

    if is_directed(G):
        graph_type = "Directed"
        scc = nx.number_strongly_connected_components(G)
        wcc = nx.number_weakly_connected_components(G)
        reciprocity = nx.reciprocity(G)
        diameter = "Can not calculate in directed graph."
        num_components = "Can not calculate in directed graph."
    else:
        graph_type = "Undirected"
        scc = "Can not calculate in undirected graph."
        wcc = "Can not calculate in undirected graph."
        reciprocity = "Can not calculate in undirected graph."
        diameter = nx.diameter(G)
        num_components = nx.number_connected_components(G)

    density = nx.density(G)
    transitivity = nx.transitivity(G)
    number_of_edges = nx.number_of_edges(G)
    number_of_nodes = nx.number_of_nodes(G)
    avg_deg = float(number_of_edges) / number_of_nodes
    try:
        dag_longest_path_length = nx.dag_longest_path_length(G)
    except Exception:
        # Graph contains a cycle or graph changed during iteration
        dag_longest_path_length = "NaN"

    average_clustering = nx.average_clustering(G)
    degree_assortativity_coefficient = nx.degree_assortativity_coefficient(G)

    try:
        radius = nx.algorithms.distance_measures.radius(G)
    except Exception as ex:
        radius = f"NaN {ex}"

    end_time = time.time()
    elapsed_time = end_time - start_time
    report_time = start_time

    if format == "stdout":
        print(f"Report Time : {report_time}")
        print(f"Elapsed Time Calculation Report : {elapsed_time}")
        print(f"Graph Type: {graph_type}")
        print(f"Graph Nodes: {number_of_nodes}")
        print(f"Graph Edges: {number_of_edges}")
        print(f"Graph Average Degree : {avg_deg}")
        print(f"Graph Density : {density}")
        print(f"Graph Transitivity : {transitivity}")
        print(f"Graph max path length : {dag_longest_path_length}")
        print(f"Graph Average Clustering Coefficient : {average_clustering}")
        print(
            f"Graph Degree Assortativity Coefficient : {degree_assortativity_coefficient}"
        )
        print(f"Graph Radius : {radius}")
        print(f"SCC: {scc}")
        print(f"WCC: {wcc}")
        print(f"Reciprocity : {reciprocity}")
        print(f"Graph Diameter : {diameter}")
        print(f"Number of Components : {num_components}")

        # bet_cen = nx.betweenness_centrality(G)
        # clo_cen = nx.closeness_centrality(G)
        # eig_cen = nx.eigenvector_centrality(G)
        # print(f'Graph Betweenness Centrality: {get_top_keys(bet_cen,1)}')
        # print(f'Graph Closeness Centrality: {get_top_keys(clo_cen,1)}')
        # print(f'Graph Eigenvector Centrality : {get_top_keys(eig_cen, 1)}')
    elif format == "json":
        data = {
            "Report Time": report_time,
            "Elapsed Time Calculation Report": elapsed_time,
            "Graph Type": graph_type,
            "Graph Nodes": number_of_nodes,
            "Graph Edges": number_of_edges,
            "Graph Average Degree": avg_deg,
            "Graph Density": density,
            "Graph Transitivity": transitivity,
            "Graph max path length": dag_longest_path_length,
            "Graph Average Clustering Coefficient": average_clustering,
            "Graph Degree Assortativity Coefficient": degree_assortativity_coefficient,
            "Graph Radius": radius,
            "SCC": scc,
            "WCC": wcc,
            "Reciprocity": reciprocity,
            "Graph Diameter": diameter,
            "Number of Components": num_components,
        }
        return data
    elif format == "string":
        rep = ""
        rep += f"Report Time : {report_time}"
        rep += f"Elapsed Time Calculation Report : {elapsed_time}"
        rep += f"Graph Type: {graph_type}"
        rep += f"Graph Nodes: {number_of_nodes}"
        rep += f"Graph Edges: {number_of_edges}"
        rep += f"Graph Average Degree : {avg_deg}"
        rep += f"Graph Density : {density}"
        rep += f"Graph Transitivity : {transitivity}"
        rep += f"Graph max path length : {dag_longest_path_length}"
        rep += f"Graph Average Clustering Coefficient : {average_clustering}"
        rep += f"""Graph Degree
          Assortativity Coefficient : {degree_assortativity_coefficient}"""
        rep += f"Graph Radius : {radius}"
        rep += f"SCC: {scc}"
        rep += f"WCC: {wcc}"
        rep += f"Reciprocity : {reciprocity}"
        rep += f"Graph Diameter : {diameter}"
        rep += f"Number of Components : {num_components}"
        return rep
    else:
        pass
