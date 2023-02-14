



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