import sys
from typing import Optional

import click
from triplea.config.settings import SETTINGS
from triplea.service.click_logger import logger
from triplea.schemas.node import Edge, Node
from triplea.schemas.article import  Article
import triplea.service.repository.state as state_manager

from triplea.service.repository.persist import  create_article, create_edge, create_node, get_all_article_count, get_all_edge_count, get_all_node_count, get_all_nodes, get_article_by_pmid, get_article_by_state, get_article_group_by_state, get_article_pmid_list_by_state, insert_new_pmid, refresh, update_article_by_pmid


tps_limit = SETTINGS.AAA_TPS_LIMIT

# It is no longer used
def _create_knowledge(article: Article):
    article.State = 5
    nodes = []
    edges = []

    node_article = Node()
    node_article.Identifier = article.PMID
    node_article.Name = article.PMID
    node_article.Type = 'Article'
    nodes.append(node_article)

    for author in article.Authors:
        node_author = Node()
        node_author.Identifier = author.HashID
        node_author.Name = author.FullName
        node_author.Type = 'Author'
        nodes.append(node_author)

        edge = Edge()
        edge.SourceID = node_author.Identifier
        edge.DestinationID = node_article.Identifier
        edge.Type = 'AUTHOR_OF'
        edge.HashID =  str(hash(edge.SourceID + edge.DestinationID))
        edges.append(edge)

        # Creating a graph of authors and affiliation.
        if author.Affiliations is not None:
            for aff in author.Affiliations:
                node_affiliation = Node()
                node_affiliation.Identifier = aff.HashID
                node_affiliation.Name = aff.Part1
                node_affiliation.Type = 'Affiliation'
                nodes.append(node_affiliation)

                edge = Edge()
                edge.SourceID = node_author.Identifier
                edge.DestinationID = node_affiliation.Identifier
                edge.Type = 'IS_MEMBER_OF'
                edge.HashID =  str(hash(edge.SourceID + edge.DestinationID))
                edges.append(edge)

    # Creating a graph of articles and keywords.
    for key in article.Keywords:
        node_keyword = Node()
        node_keyword.Identifier = key.Text
        node_keyword.Name = key.Text
        node_keyword.Type = 'Keyword'
        nodes.append(node_keyword)

        edge = Edge()
        edge.SourceID = node_article.Identifier
        edge.DestinationID = node_keyword.Identifier
        edge.Type = 'KEYWORD'
        edge.HashID =  str(hash(edge.SourceID + edge.DestinationID))
        edges.append(edge)

    # Creating a graph of articles and references.
    if article.References is not None:
        for ref in article.References:
            node_reference = Node()
            node_reference.Identifier = ref
            node_reference.Name = ref
            node_reference.Type = 'Article'
            nodes.append(node_reference)

            edge = Edge()
            edge.SourceID = node_article.Identifier
            edge.DestinationID = node_reference.Identifier
            edge.Type = 'REFERENCE'
            edge.HashID =  str(hash(edge.SourceID + edge.DestinationID))
            edges.append(edge)              


    # Save node & edge to db
    for n in nodes:
        create_node(n)
    
    for e in edges:
        create_edge(e)

    return article

# It is no longer used
def _extract_knowledge(article: Article):   
    article.State = 5
    nodes = []
    edges = []

    node_article = Node()
    node_article.Identifier = article.PMID
    node_article.Name = article.PMID
    node_article.Type = 'Article'
    nodes.append(node_article)

    for author in article.Authors:
        node_author = Node()
        node_author.Identifier = author.HashID
        node_author.Name = author.FullName
        node_author.Type = 'Author'
        nodes.append(node_author)

        edge = Edge()
        edge.SourceID = node_author.Identifier
        edge.DestinationID = node_article.Identifier
        edge.Type = 'AUTHOR_OF'
        edge.HashID =  str(hash(edge.SourceID + edge.DestinationID))
        edges.append(edge)

        # Creating a graph of authors and affiliation.
        if author.Affiliations is not None:
            for aff in author.Affiliations:
                node_affiliation = Node()
                node_affiliation.Identifier = aff.HashID
                node_affiliation.Name = aff.Part1
                node_affiliation.Type = 'Affiliation'
                nodes.append(node_affiliation)

                edge = Edge()
                edge.SourceID = node_author.Identifier
                edge.DestinationID = node_affiliation.Identifier
                edge.Type = 'IS_MEMBER_OF'
                edge.HashID =  str(hash(edge.SourceID + edge.DestinationID))
                edges.append(edge)
 
    # Creating a graph of articles and keywords.
    for key in article.Keywords:
        node_keyword = Node()
        node_keyword.Identifier = key.Text
        node_keyword.Name = key.Text
        node_keyword.Type = 'Keyword'
        nodes.append(node_keyword)

        edge = Edge()
        edge.SourceID = node_article.Identifier
        edge.DestinationID = node_keyword.Identifier
        edge.Type = 'KEYWORD'
        edge.HashID =  str(hash(edge.SourceID + edge.DestinationID))
        edges.append(edge)

    # Creating a graph of articles and references.
    if article.References is not None:
        for ref in article.References:
            node_reference = Node()
            node_reference.Identifier = ref
            node_reference.Name = ref
            node_reference.Type = 'Article'
            nodes.append(node_reference)

            edge = Edge()
            edge.SourceID = node_article.Identifier
            edge.DestinationID = node_reference.Identifier
            edge.Type = 'REFERENCE'
            edge.HashID =  str(hash(edge.SourceID + edge.DestinationID))
            edges.append(edge)

    return { 'nodes' : nodes, 'edges' : edges}

def move_state_forward(state: int,
                       tps_limit: Optional[int] = 1,
                       extend_by_refrence: Optional[bool] = False,
                       extend_by_cited: Optional[bool] = False):
    """
    It takes an article, extracts the data from it, and then creates a node and edge for each author and
    affiliation
    
    :param state: The state of the article in Knowledge Repository you want to move forward
    :type state: int
    :param tps_limit: The number of requests per second you want to make to the API, defaults to 1
    :type tps_limit: Optional[int] (optional)
    """

    # la = get_article_by_state(state) # old version
    l_pmid = get_article_pmid_list_by_state(state)
    total_article_in_current_state = len(l_pmid)
    number_of_article_move_forward = 0
    logger.DEBUG(str(len(l_pmid)) + ' Article(s) is in state ' + str(state))

    bar  = click.progressbar(length=len(l_pmid), show_pos=True,show_percent =True) 


    refresh_point = 0
    for id in l_pmid:
        try:
            number_of_article_move_forward = number_of_article_move_forward + 1
            current_state = None
            
            if refresh_point == 500:
                refresh_point = 0
                refresh()
                print()
                logger.INFO(f'There are {str(total_article_in_current_state - number_of_article_move_forward)} article(s) left ', forecolore='yellow')
                min = (total_article_in_current_state - number_of_article_move_forward) / 60
                logger.INFO(f'It takes at least {str(int(min))} minutes or {str(int(min/60))} hours', forecolore='yellow')
            else:
                refresh_point = refresh_point + 1

            a = get_article_by_pmid(id)
            try:
                updated_article = Article(**a.copy())
            except:
                # print()
                # backward_dict = a.copy()
                # backward = Article()
                # backward.PMID = backward_dict['PMID']
                # logger.ERROR(f'Error in parsing article. PMID = {backward.PMID}')
                # backward.State = 0
                # updated_article = backward
                # l = update_article_by_pmid(updated_article , updated_article.PMID)
                print()
                print(logger.ERROR(f'Error in parsing article. PMID = {id}'))
                raise Exception('Article Not Parsed.')


            try:
                current_state = updated_article.State
            except:
                current_state = 0

            # logger.DEBUG('Article ' + updated_article.PMID + ' with state ' + str(current_state) + ' forward to ' + str(current_state + 1))
            bar.label = 'Article ' + updated_article.PMID + ' with state ' + str(current_state) + ' forward to ' + str(current_state + 1)
            bar.update(1)
            ## for re run
            # if current_state == 2 : current_state = 1

            if current_state is None:
                updated_article = state_manager.expand_details(updated_article)
                l = update_article_by_pmid(updated_article , updated_article.PMID)

            elif current_state == -1: # Error in State 0 Net state: 1
                updated_article = state_manager.parsing_details(updated_article)
                l = update_article_by_pmid(updated_article , updated_article.PMID)

            elif current_state == 0: # Net state: get article details from pubmed
                updated_article = state_manager.expand_details(updated_article)
                l = update_article_by_pmid(updated_article , updated_article.PMID)
                    
            elif current_state == 1: # Net state: Extract Data
                updated_article = state_manager.parsing_details(updated_article)
                l = update_article_by_pmid(updated_article , updated_article.PMID)
                # # think after
                # if len(l) == 1:
                #     pass
                # else:
                #     logger.ERROR('Duplication has Occurred')

            elif current_state == 2: # Net state: Get Citation
                updated_article = state_manager.get_citation(updated_article)
                l = update_article_by_pmid(updated_article , updated_article.PMID)
                # think after
                # if len(l) == 1:
                #     pass
                # else:
                #     logger.ERROR('Duplication has Occurred')

            elif current_state == 3: # Net state: NER Title 
                updated_article = state_manager.ner_title(updated_article)
                l = update_article_by_pmid(updated_article , updated_article.PMID)
                # think after
                # if len(l) == 1:
                #     pass
                # else:
                #     logger.ERROR('Duplication has Occurred')

            elif current_state == 4: # Net state:Create Knowledge
                updated_article = _create_knowledge(updated_article)
                # l = update_article_by_pmid(updated_article , updated_article.PMID)

            else:
                raise NotImplementedError

        except:
            if current_state == 1: 
                updated_article = Article(**a.copy())  
                updated_article.State = -1
                update_article_by_pmid(updated_article , updated_article.PMID)
                refresh()
                exc_type, exc_value, exc_tb = sys.exc_info()
                logger.ERROR(f'Error {exc_type}')
                logger.ERROR(f'Error {exc_value}')

            elif current_state is None:
                # Article Not Parsed.
                print()
                refresh()
                exc_type, exc_value, exc_tb = sys.exc_info()
                logger.ERROR(f'Error {exc_type}')
                logger.ERROR(f'Error {exc_value}')

            elif current_state == 2: 
                updated_article = Article(**a.copy())  
                updated_article.State = -2
                raise
                update_article_by_pmid(updated_article , updated_article.PMID)
                refresh()
                exc_type, exc_value, exc_tb = sys.exc_info()
                print()
                logger.ERROR(f'Error {exc_type}')
                logger.ERROR(f'Error {exc_value}')

            else:
                refresh()
                exc_type, exc_value, exc_tb = sys.exc_info()
                
                print()
                print(exc_tb.tb_lineno)
                raise

                logger.ERROR(f'Error {exc_type}')
                logger.ERROR(f'Error {exc_value}')

if __name__ == '__main__':
    logger.WARNING('Number of article in knowlege repository is ' + str(get_all_article_count()))
    logger.WARNING(f'{get_all_node_count()} Node(s) in knowlege repository.')
    logger.WARNING(f'{get_all_edge_count()} Edge(s) in knowlege repository.')
    data = get_article_group_by_state()
    for i in range(-3,7):
        w = 0
        for s in data:
            if s['State'] == i:
                w = 1
                n = s['n']
                logger.INFO(f'{n} article(s) in state {i}.')
        if w == 0 : 
            logger.INFO(f'0 article(s) in state {i}.')



    # s = '("Breast Neoplasms"[Mesh] OR "Breast Cancer"[Title] OR "Breast Neoplasms"[Title] OR "Breast Neoplasms"[Other Term] OR "Breast Cancer"[Other Term]) AND ("Registries"[MeSH Major Topic] OR "Database Management Systems"[MeSH Major Topic] OR "Information Systems"[MeSH Major Topic] OR "Registry"[Other Term] OR "Registry"[Title] OR "Information Storage and Retrieval"[MeSH Major Topic])'
    # get_article_list_all_store_to_kg_rep(s)

    # move_state_forward(3)
    # refresh()

    # data = get_article_by_pmid('35130239')
    # data= json.dumps(data, indent=4)
    # with open("one-35130239.json", "w") as outfile:
    #     outfile.write(data)

    # 32434767
    # click.echo(click.style('Number of article in knowlege repository is ', fg='green') + ' ' + click.style(str(get_all_article_count()), fg='red'))
    # click.secho('Hello World!', fg='green')
    # click.secho('Some more text', bg='blue', fg='white')
    # click.secho('ATTENTION', blink=True, bold=True)

    
    # # Save Title for Annotation
    # file =  open("article-title.txt", "w",  encoding="utf-8")
    # la = get_article_by_state(2)
    # for a in la:
    #     try:
    #         article = Article(**a.copy())
    #     except:
    #         pass
    #     file.write(article.Title + "\n")

    # # Get list of cited article
    # data = get_cited_article_from_pubmed('26951748')
    # data = json.dumps(data, indent=4)
    # with open("one-cite.json", "w") as outfile:
    #     outfile.write(data)

    
    # print(insert_new_pmid('36619805',
    #                             reference_crawler_deep=SETTINGS.AAA_REFF_CRAWLER_DEEP,
    #                             cite_crawler_deep=SETTINGS.AAA_CITED_CRAWLER_DEEP))

    # refresh()








        




    

   
