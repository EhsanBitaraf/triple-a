# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=("Electronic+Health+Records"[Mesh])+AND+("National"[Title/Abstract])&retmode=json&retstart=${esearchresultRetstart}&retmax=10000

# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=${PMID.0}&retmode=xml
import json
import time
from typing import Optional
import requests
import tinydb
import xmltodict
import click
from triplea.schemas.node import Edge, Node


from triplea.service.click_logger import logger
# from config.settings import ROOT,SETTINGS
from triplea.config.settings import ROOT,SETTINGS
from triplea.schemas.article import Affiliation, Article, Author
from triplea.service.persist import create_article, create_edge, create_node, get_all_article_count, get_all_edge_count, get_all_node_count, get_all_nodes, get_article_by_pmid, get_article_by_state, insert_new_pmid, update_article_by_pmid

def get_article_list_from_pubmed(retstart:int, retmax:int, search_term:str)-> dict:
    """
    This function takes in a search term, and returns a dictionary of the results of the search
    
    :param retstart: The index of the first article to return
    :type retstart: int
    :param retmax: The maximum number of articles to return
    :type retmax: int
    :param search_term: the search term you want to use to search for articles
    :type search_term: str
    :return: A dictionary with the following keys:
    """
    # api-endpoint
    # [api-endpoint help][https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch]
    URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
    
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'db': 'pubmed', # https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch
            'term': search_term ,  # Entrez text query. All special characters must be URL encoded. Spaces may be replaced by '+' signs. For very long queries (more than several hundred characters long), consider using an HTTP POST call. See the PubMed or Entrez help for information about search field descriptions and tags. Search fields and tags are database specific.
            'retmode':'json' , # Retrieval type. Determines the format of the returned output. The default value is ‘xml’ for ESearch XML, but ‘json’ is also supported to return output in JSON format.
            'retstart': retstart, # Sequential index of the first UID in the retrieved set to be shown in the XML output (default=0, corresponding to the first record of the entire set). This parameter can be used in conjunction with retmax to download an arbitrary subset of UIDs retrieved from a search.
            'retmax' : retmax, # Total number of UIDs from the retrieved set to be shown in the XML output (default=20). By default, ESearch only includes the first 20 UIDs retrieved in the XML output. If usehistory is set to 'y', the remainder of the retrieved set will be stored on the History server; otherwise these UIDs are lost. Increasing retmax allows more of the retrieved UIDs to be included in the XML output, up to a maximum of 10,000 records.
            }
    # sending get request and saving the response as response object
    try:
        r = requests.get(url = URL, params = PARAMS)
    except:
        raise Exception('Connection Error.')

    # extracting data in json format
    data = r.json()
    return data

def get_article_details_from_pubmed(PMID)->dict:
    URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
    PARAMS = {'db': 'pubmed',
            'id': PMID , 
            'retmode':'xml' ,
            }
    r = requests.get(url = URL, params = PARAMS)
    if r.status_code == 200:
        xml = r.content
        data_dict = xmltodict.parse(xml)
        return data_dict
    else:
        raise Exception('Error')

def save_article_pmid_list_in_kgrep(data:dict)-> None:
    """
    > If the data is in the right format, then for each PMID in the data, insert the PMID into the
    knowledge repository. If the PMID is not a duplicate, then log the PMID as added to the knowledge
    repository
    
    :param data: dict
    :type data: dict
    """
    if 'esearchresult' in data:
        qt = data['esearchresult']['querytranslation']
        for pmid in data['esearchresult']['idlist']:
            i = insert_new_pmid(pmid, qt)
            if i is None: # PMID is Duplicate
                logger.INFO( pmid + ' is exist in knowledge repository.')
            else:
                logger.INFO('add ' + pmid + ' to knowledge repository. get ' + str(i))
    else:
        logger.ERROR('data is not in right format.')

def main():
    # Opening JSON file
    f = open('sample.json')
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    
    # Iterating through the json
    # list
    for i in data['esearchresult']['idlist']:
        a = Article(PMID = i)
        create_article(a)
        print(i)
    
    # Closing file
    f.close()


def get_article_list_all_store_to_kg_rep(searchterm:str,
                                         tps_limit: Optional[int] = 1,
                                         big_ret: Optional[bool] = True,
                                         retmax: Optional[int] = 10000,
                                         ):

    sleep_time = 1  // tps_limit
    data = get_article_list_from_pubmed(0 ,1 , searchterm)
    ## file base test
    # f = open('sample1.json')
    # data = json.load(f)
    # f.close()

    total = int(data['esearchresult']['count'])
    logger.INFO('Total number of article is ' + str(total))

    if big_ret == True:
        retmax = 10000
    else:
        retmax = 20
    
    if total >= retmax:
        round = total // retmax
    else : # total < retmax
        retmax = total
        round = 2

    for i in range(1 , round):
        time.sleep(sleep_time)
        logger.INFO('Round (' + str(i) + ') : ' + 'Get another ' + str(retmax) + ' record (Total ' + str(i * retmax) + ' record)', deep = 13)
        start = (i * retmax) - retmax
        chunkdata = get_article_list_from_pubmed(start , retmax ,searchterm)
        save_article_pmid_list_in_kgrep(chunkdata)

    # for last round
    start = ((i + 1) * retmax) - retmax
    mid = total - (retmax * round)
    logger.INFO('Round (' + str(i+1) + ') : ' + 'Get another ' + str(mid) + ' record (total ' + str(total) + ' record)', deep = 13)
    chunkdata = get_article_list_from_pubmed(start , retmax ,searchterm)
    save_article_pmid_list_in_kgrep(chunkdata)

def move_state_forward(state: int):
    la = get_article_by_state(state)
    logger.DEBUG(str(len(la)) + ' Article(s) is in state ' + str(state))
    for a in la:
        updated_article = Article(**a.copy()) 
        
        try:
            current_state = updated_article.State
        except:
            current_state = 0
        logger.DEBUG('Article ' + updated_article.PMID + ' with state ' + str(current_state) + ' forward to ' + str(current_state + 1))

        ## for re run
        # if current_state == 2 : current_state = 1


        if current_state is None:
            updated_article.State = 1
            time.sleep(3)
            oa = get_article_details_from_pubmed(updated_article.PMID)
            updated_article.OreginalArticle = oa
            l = update_article_by_pmid(updated_article , updated_article.PMID)

        elif current_state == 0:
            updated_article.State = 1
            time.sleep(3)
            oa = get_article_details_from_pubmed(updated_article.PMID)
            updated_article.OreginalArticle = oa
            l = update_article_by_pmid(updated_article , updated_article.PMID)
                  
        elif current_state == 1: # Extract Data
            updated_article.State = 2
            data = updated_article.OreginalArticle
            PubmedData = data['PubmedArticleSet']['PubmedArticle']['PubmedData']
            
            ArticleId = PubmedData['ArticleIdList']['ArticleId']
            for a_id in ArticleId:
                if a_id['@IdType'] == 'doi':
                    updated_article.DOI = a_id['#text']
            
            pubmed_article_data = data['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']
            updated_article.Title =  pubmed_article_data['ArticleTitle']
            updated_article.Journal = pubmed_article_data['Journal']['Title']

            if 'Abstract' in pubmed_article_data:
                if type(pubmed_article_data['Abstract']) == dict:
                    if type(pubmed_article_data['Abstract']['AbstractText']) == str:
                        updated_article.Abstract = pubmed_article_data['Abstract']['AbstractText']
                    elif type(pubmed_article_data['Abstract']['AbstractText']) == list:
                        abstract_all = ''
                        for abstract_part in pubmed_article_data['Abstract']['AbstractText']:
                            abstract_all = abstract_all + ' ' + abstract_part['#text']
                        updated_article.Abstract = abstract_all
                    else:
                        raise NotImplementedError
                else:
                    raise NotImplementedError

            author_list=[]
            for author in pubmed_article_data['AuthorList']['Author']:
                my_author = Author()
                my_author.ForeName = author['ForeName']
                my_author.LastName = author['LastName']
                my_author.FullName = my_author.ForeName + ' ' + my_author.LastName
                if 'Identifier' in author:
                    if author['Identifier']['@Source'] == 'ORCID':
                        my_author.ORCID = author['Identifier']['#text']

                if 'AffiliationInfo' in author:
                    affiliation_list = []
                    if type(author['AffiliationInfo']) == dict:
                        affiliation = Affiliation()
                        affiliation.Text = author['AffiliationInfo']['Affiliation']
                        aff_part = affiliation.Text.split(',')
                        aff_part_number = len(aff_part)
                        affiliation.Part1 = aff_part[0]
                        affiliation.Has_Extra = False
                        if aff_part_number > 1 : affiliation.Part2 = aff_part[1].strip()
                        if aff_part_number > 2 : affiliation.Part3 = aff_part[2].strip()
                        if aff_part_number > 3 : affiliation.Part4 = aff_part[3].strip()
                        if aff_part_number > 4 : affiliation.Part5 = aff_part[4].strip()
                        if aff_part_number > 5 : affiliation.Part6 = aff_part[5].strip()
                        if aff_part_number > 6 :
                            affiliation.Has_Extra = True
                            

                        pre_hash = str(affiliation.Part1) + str(affiliation.Part2) + str(affiliation.Part3) + str(affiliation.Part4)
                        affiliation.HashID = str(hash(pre_hash))
                        affiliation_list.append (affiliation)

                    elif type(author['AffiliationInfo']) == list:
                        for aff in  author['AffiliationInfo']:
                            affiliation = Affiliation()
                            affiliation.Text = aff['Affiliation']
                            aff_part = affiliation.Text.split(',')
                            aff_part_number = len(aff_part)
                            affiliation.Part1 = aff_part[0]
                            affiliation.Has_Extra = False
                            if aff_part_number > 1 : affiliation.Part2 = aff_part[1].strip()
                            if aff_part_number > 2 : affiliation.Part3 = aff_part[2].strip()
                            if aff_part_number > 3 : affiliation.Part4 = aff_part[3].strip()
                            if aff_part_number > 4 : affiliation.Part5 = aff_part[4].strip()
                            if aff_part_number > 5 : affiliation.Part6 = aff_part[5].strip()
                            if aff_part_number > 6 :
                                affiliation.Has_Extra = True
                                
                            pre_hash = str(affiliation.Part1) + str(affiliation.Part2) + str(affiliation.Part3) + str(affiliation.Part4)
                            affiliation.HashID = str(hash(pre_hash))
                            affiliation_list.append (affiliation)
                    else:
                        raise NotImplementedError

                    my_author.Affiliations = affiliation_list

            
                my_author.HashID = str(hash(my_author.FullName))
                author_list.append(my_author)

            updated_article.Authors = author_list
            l = update_article_by_pmid(updated_article , updated_article.PMID)
            if len(l) == 1:
                pass
            else:
                logger.ERROR('Duplication has Occurred')

        elif current_state == 2: # Create Knowlege
            updated_article.State = 3
            nodes = []
            edges = []

            node_article = Node()
            node_article.Identifier = updated_article.PMID
            node_article.Name = updated_article.PMID
            node_article.Type = 'Article'
            nodes.append(node_article)

            for author in updated_article.Authors:
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
                

            # Save node & edge to db
            for n in nodes:
                create_node(n)
            
            for e in edges:
                create_edge(e)
            



        else:
            raise NotImplementedError

if __name__ == '__main__':
    logger.WARNING('Number of article in knowlege repository is ' + str(get_all_article_count()))

    # move_state_forward(2)
    print(get_all_node_count())
    print(get_all_edge_count())

    print(type(get_all_nodes()))




    # 32434767
    # click.echo(click.style('Number of article in knowlege repository is ', fg='green') + ' ' + click.style(str(get_all_article_count()), fg='red'))
    # click.secho('Hello World!', fg='green')
    # click.secho('Some more text', bg='blue', fg='white')
    # click.secho('ATTENTION', blink=True, bold=True)

    

    

   







    




    