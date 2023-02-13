import json
from logging import info
import sys
import time
from typing import Optional
import requests
import xmltodict
from triplea.service.click_logger import logger
from triplea.schemas.node import Edge, Node

from triplea.config.settings import ROOT,SETTINGS
from triplea.schemas.article import Affiliation, Article, Author, Keyword, NamedEntity
from triplea.service.ner import get_title_ner
from triplea.service.persist import  create_article, create_edge, create_node, get_all_article_count, get_all_edge_count, get_all_node_count, get_all_nodes, get_article_by_pmid, get_article_by_state, get_article_group_by_state, get_article_pmid_list_by_state, insert_new_pmid, refresh, update_article_by_pmid


tps_limit = SETTINGS.AAA_TPS_LIMIT


def _convert_dict_to_class_affiliation(data:dict)-> Affiliation:
    """
    It takes a dictionary as input, and returns an Affiliation object
    
    :param data: dict
    :type data: dict
    :return: an Affiliation object
    """
    affiliation = Affiliation()
    affiliation.Text = data['Affiliation']
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
    return affiliation

def _convert_dict_to_class_author(data:dict)-> Author:
    """
    It takes a dictionary and returns an Author object
    
    :param data: dict
    :type data: dict
    :return: an Author object
    """
    if 'CollectiveName' in data:
        my_author = Author()
        my_author.FullName = data['CollectiveName']
        my_author.HashID = str(hash(my_author.FullName))
        return my_author

    my_author = Author()
    my_author.ForeName = data['ForeName']
    my_author.LastName = data['LastName']
    my_author.FullName = my_author.ForeName + ' ' + my_author.LastName
    my_author.HashID = str(hash(my_author.FullName))
    if 'Identifier' in data:
        if data['Identifier']['@Source'] == 'ORCID':
            my_author.ORCID = data['Identifier']['#text']


    if 'AffiliationInfo' in data:
        affiliation_list = []
        if type(data['AffiliationInfo']) == dict:
            affiliation = _convert_dict_to_class_affiliation(data['AffiliationInfo'])
            affiliation_list.append(affiliation)
        elif type(data['AffiliationInfo']) == list:
            for aff in  data['AffiliationInfo']:
                affiliation = _convert_dict_to_class_affiliation(aff)
                affiliation_list.append(affiliation)
        else:
            raise NotImplementedError
        
        my_author.Affiliations = affiliation_list
    
    return my_author

def _convert_dict_to_class_keyword(data:dict) -> Keyword:
    my_keyword = Keyword()
    my_keyword.Text = data['#text']
    if ',' in my_keyword.Text:
        raise NotImplementedError 
    if data['@MajorTopicYN'] == 'Y':
        my_keyword.IS_Major = True
    else:
        my_keyword.IS_Major = False
    my_keyword.IS_Mesh = False
    return my_keyword

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

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}

    # To use HTTP Basic Auth with your proxy, use the http://user:password@host.com/ syntax:
    if SETTINGS.AAA_PROXY_HTTP is not None:
        proxy_servers = {
            'http': SETTINGS.AAA_PROXY_HTTP,
            'https': SETTINGS.AAA_PROXY_HTTPS,
            }
    else:
        proxy_servers = None


    # sending get request and saving the response as response object
    try:
        r = requests.get(url = URL, params = PARAMS , headers= headers , proxies = proxy_servers )
    except:
        raise Exception('Connection Error.')

    # extracting data in json format
    data = r.json()
    return data

def get_article_details_from_pubmed(PMID)->dict:
    """
    It takes a PMID as input and returns a dictionary of the article's details from Pubmed
    
    :param PMID: The PubMed ID of the article you want to get the details of
    :return: It returns a dictionary that is converted from the [XML output](https://www.nlm.nih.gov/bsd/licensee/elements_descriptions.html) of the pubmed site to the json model
    """
    URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
    PARAMS = {'db': 'pubmed',
            'id': PMID , 
            'retmode':'xml' ,
            }

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}

    # To use HTTP Basic Auth with your proxy, use the http://user:password@host.com/ syntax:
    if SETTINGS.AAA_PROXY_HTTP is not None:
        proxy_servers = {
            'http': SETTINGS.AAA_PROXY_HTTP,
            'https': SETTINGS.AAA_PROXY_HTTPS,
            }
    else:
        proxy_servers = None

    r = requests.get(url = URL, params = PARAMS, headers= headers , proxies = proxy_servers)
    if r.status_code == 200:
        xml = r.content
        data_dict = xmltodict.parse(xml)
        return data_dict
    else:
        raise Exception('Error')

def get_cited_article_from_pubmed(PMID)->dict:
    URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?"
    PARAMS = {'dbfrom': 'pubmed',
               'db': 'pubmed',
                'id': PMID , 
                'retmode':'json' ,
            }

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'}

    # To use HTTP Basic Auth with your proxy, use the http://user:password@host.com/ syntax:
    if SETTINGS.AAA_PROXY_HTTP is not None:
        proxy_servers = {
            'http': SETTINGS.AAA_PROXY_HTTP,
            'https': SETTINGS.AAA_PROXY_HTTPS,
            }
    else:
        proxy_servers = None

    r = requests.get(url = URL, params = PARAMS, headers= headers , proxies = proxy_servers)
    if r.status_code == 200:
        # xml = r.content
        # data_dict = xmltodict.parse(xml)
        data_byte = r.content # it is byte
        
        data = json.loads(data_byte.decode('utf-8'))
        if 'linksets' in data:
            for link in data['linksets']:
                # print(type(link))
                # print(type(link['linksetdbs']))
                for linkdb in link['linksetdbs']:
                    rd = linkdb['linkname']
                    if rd == 'pubmed_pubmed' or rd =='pubmed_pubmed_alsoviewed' or  rd == 'pubmed_pubmed_combined' or rd == 'pubmed_pubmed_five' or rd == 'pubmed_pubmed_reviews' or rd == 'pubmed_pubmed_reviews_five' :
                        pass
                    else:
                        # print(linkdb['linkname'])
                        pass
                    if linkdb['linkname'] == 'pubmed_pubmed_citedin':
                        return linkdb['links']
        else:
            raise
    else:
        raise Exception('Error')


def save_article_pmid_list_in_kgrep(data:dict)-> None:
    """
    > If the data is in the right format, then for each PMID in the data, insert the PMID into the
    knowledge repository. If the PMID is not a duplicate, then log the PMID as added to the knowledge
    repository
    
    :param data: The output format from the pubmed service is for a list of PMIDs that is output from the `get_article_list_from_pubmed` method.
    :type data: dict
    """
    if 'esearchresult' in data:
        qt = data['esearchresult']['querytranslation']
        for pmid in data['esearchresult']['idlist']:
            i = insert_new_pmid(pmid,
                                querytranslation= qt ,
                                reference_crawler_deep=SETTINGS.AAA_REFF_CRAWLER_DEEP,
                                cite_crawler_deep=SETTINGS.AAA_CITED_CRAWLER_DEEP)
            if i is None: # PMID is Duplicate
                logger.INFO( pmid + ' is exist in knowledge repository.')
            else:
                logger.INFO('add ' + pmid + ' to knowledge repository. get ' + str(i))
    else:
        logger.ERROR('data is not in right format.')

def get_article_list_all_store_to_kg_rep(searchterm:str,
                                         tps_limit: Optional[int] = 1,
                                         big_ret: Optional[bool] = True,
                                         retmax: Optional[int] = 10000,
                                         )-> None:
    """
    It takes a search term, and returns a list of all the articles that match that search term
    
    :param searchterm: The search term you want to use to search PubMed
    :type searchterm: str
    :param tps_limit: The number of requests per second, defaults to 1
    :type tps_limit: Optional[int] (optional)
    :param big_ret: If True, the function will return a maximum of 10,000 records. If False, it will
    return a maximum of 20 records, defaults to True
    :type big_ret: Optional[bool] (optional)
    :param retmax: The number of articles to return per request, defaults to 10000
    :type retmax: Optional[int] (optional)
    """
    sleep_time = 1  // tps_limit
    data = get_article_list_from_pubmed(0 ,2 , searchterm)

    total = int(data['esearchresult']['count'])
    logger.INFO('Total number of article is ' + str(total))

    if total == 0:
        return 

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

def _check_extention(extend_by_refrence:bool, extend_by_cited:bool, article_insert_type:list[str]):
    pass

def _expand_details( article: Article):
    article.State = 1
    sleep_time = 1  // tps_limit
    time.sleep(sleep_time)
    try:
        oa = get_article_details_from_pubmed(article.PMID)
        article.OreginalArticle = oa
    except:
        article.State = 0
        exc_type, exc_value, exc_tb = sys.exc_info()
        logger.ERROR(f'Error {exc_type} Value : {exc_value}')
        logger.ERROR(f'Error {exc_tb}')


    return article

def _parsing_details(article: Article):
    article.State = 2
    data = article.OreginalArticle
    PubmedData = data['PubmedArticleSet']['PubmedArticle']['PubmedData']
    
    # The above code is checking if the article has a DOI or PMC number. If it does, it will update the
    # article with the DOI or PMC number.
    if 'ArticleIdList' in PubmedData:
        ArticleId = PubmedData['ArticleIdList']['ArticleId']
        if type(ArticleId) == list:
            for a_id in ArticleId:
                if a_id['@IdType'] == 'doi':
                    article.DOI = a_id['#text']
                if a_id['@IdType'] == 'pmc':
                    article.PMC = a_id['#text']
        elif type(ArticleId) == dict:
                if ArticleId['@IdType'] == 'doi':
                    article.DOI = a_id['#text']
                if ArticleId['@IdType'] == 'pmc':
                    article.PMC = a_id['#text']
        else:
            raise NotImplementedError

    # update article Title & Journal Title.
    pubmed_article_data = data['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']
    article.Title =  pubmed_article_data['ArticleTitle']
    article.Journal = pubmed_article_data['Journal']['Title']
    
    # print(pubmed_article_data['ArticleDate']) ------------------------------------------------------------------------

    # The above code is checking if the abstract is a string or a list. If it is a string, it will add the
    # abstract to the database. If it is a list, it will add all the abstracts to the database.
    if 'Abstract' in pubmed_article_data:
        if type(pubmed_article_data['Abstract']) == dict:
            if type(pubmed_article_data['Abstract']['AbstractText']) == str:
                article.Abstract = pubmed_article_data['Abstract']['AbstractText']
            elif type(pubmed_article_data['Abstract']['AbstractText']) == list:
                abstract_all = ''
                for abstract_part in pubmed_article_data['Abstract']['AbstractText']:
                    abstract_all = abstract_all + ' ' + abstract_part['#text']
                article.Abstract = abstract_all
            elif type(pubmed_article_data['Abstract']['AbstractText']) == dict:
                # exception happen in pmid '36497366' one-abstract-dict-mode.json
                article.Abstract = pubmed_article_data['Abstract']['AbstractText']['#text']
            else:
                t = type(pubmed_article_data['Abstract']['AbstractText'])
                logger.ERROR (f'Type {str(t)} in Abstract Not Implemented')
                raise NotImplementedError
        else:
            raise NotImplementedError

    # Creating a list of keywords. Merging Mesh List & Keyword List
    medline_citation = data['PubmedArticleSet']['PubmedArticle']['MedlineCitation']
    keyword_list = []
    if 'MeshHeadingList' in medline_citation:
        for mesh in medline_citation['MeshHeadingList']['MeshHeading']:
            my_keyword = Keyword()
            my_keyword.Text = mesh['DescriptorName']['#text']
            if mesh['DescriptorName']['@MajorTopicYN'] == 'Y':
                my_keyword.IS_Major = True
            else:
                my_keyword.IS_Major = False
            # mesh['QualifierName'] # We did not get into this subject
            my_keyword.IS_Mesh = True
            keyword_list.append(my_keyword)
    if 'KeywordList' in medline_citation:
        if type(medline_citation['KeywordList']['Keyword']) == list:
            for keyword in medline_citation['KeywordList']['Keyword']:
                my_keyword = _convert_dict_to_class_keyword(keyword)
                keyword_list.append(my_keyword)
        elif type(medline_citation['KeywordList']['Keyword']) == dict:
            my_keyword = _convert_dict_to_class_keyword(medline_citation['KeywordList']['Keyword'])
            keyword_list.append(my_keyword)
        else:
            raise NotImplementedError

    article.Keywords = keyword_list

    # The code is parsing the Article and extracting the references from the Mode.
    if 'ReferenceList' in PubmedData:
        if article.ReferenceCrawlerDeep is None:
            # raise Exception('ReferenceCrawlerDeep is None.')
            article.ReferenceCrawlerDeep = 0
        
        if article.ReferenceCrawlerDeep > 0:
            reference_list = []
            for ref in PubmedData['ReferenceList']['Reference']:
                if 'ArticleIdList' in ref:
                    if type(ref['ArticleIdList']['ArticleId']) == dict:
                        if ref['ArticleIdList']['ArticleId']['@IdType'] == 'pubmed':
                            reference_list.append(ref['ArticleIdList']['ArticleId']['#text'])

                    elif type(ref['ArticleIdList']['ArticleId']) == list:
                        for ref_id in ref['ArticleIdList']['ArticleId']:
                            if ref_id['@IdType'] == 'pubmed':
                                reference_list.append(ref_id['#text'])
                    else:
                        raise NotImplementedError
            
            article.References = reference_list
            # create new article
            logger.DEBUG(f'Add {len(reference_list)} new article(s) by REFERENCE. ' , forecolore='yellow' , deep = 3)
            new_rcd = article.ReferenceCrawlerDeep - 1
            for ref_pmid in reference_list:
                start = time.time_ns()
                # insert_new_pmid(pmid = ref_pmid , insert_type = 'REFERENCE' , reference_crawler_deep= new_rcd)
                insert_new_pmid(pmid = ref_pmid , reference_crawler_deep= new_rcd)
                end = time.time_ns()
                # logger.DEBUG(f'Time taken {end-start} ns',forecolore= 'white' , deep = 5)

            return article
                
    if 'AuthorList' in pubmed_article_data:
        author_list=[]
        if type(pubmed_article_data['AuthorList']['Author']) == list:
            for author in pubmed_article_data['AuthorList']['Author']:
                my_author = _convert_dict_to_class_author(author)
                author_list.append(my_author)
        elif type(pubmed_article_data['AuthorList']['Author']) == dict:
            my_author = _convert_dict_to_class_author(pubmed_article_data['AuthorList']['Author'])
            author_list.append(my_author)
        else:
            raise NotImplementedError
        article.Authors = author_list
    else:
        logger.WARNING(f'Article {article.PMID} has no AuthorList',forecolore= 'white' , deep = 5)
    
    return article

def _ner_title(article: Article):
    article.State = 3
    ner = get_title_ner(article.Title)
    l_ner = []
    for e in ner:
        my_ner = NamedEntity()
        if len(e.ents) > 1: raise NotImplementedError
        my_ner.Label = e.label_
        # print(type(e.ents[0]))
        my_ner.Entity = e.ents[0].text
        l_ner.append(my_ner)
        # print(f'{e.label_} : {e.ents}')
    
    if len(l_ner) > 0:
        article.NamedEntities = l_ner

    return article

def _get_citation(article: Article):
    article.State = 4
    pmid = article.PMID
    if pmid is not None:
        if article.CiteCrawlerDeep > 0:
            try:
                lc = get_cited_article_from_pubmed(pmid)
            except:
                article.State = 3
                exc_type, exc_value, exc_tb = sys.exc_info()
                logger.ERROR(f'Error {exc_type} Value : {exc_value}')
                logger.ERROR(f'Error {exc_tb}')
                return article
        
            if lc is not None:
                if len(lc) > 0:
                    if article.CiteCrawlerDeep is None:
                        article.CiteCrawlerDeep = 0 
                        # raise Exception('CiteCrawlerDeep is None.')
                    if article.CiteCrawlerDeep > 0:
                        article.CitedBy = lc
                        # create new article
                        logger.DEBUG(f'Add {len(lc)} new article(s) by CITED.' , forecolore='yellow' , deep = 3)
                        new_ccd = article.CiteCrawlerDeep - 1
                        for c in lc:
                            insert_new_pmid(pmid = c , cite_crawler_deep= new_ccd)
        else:
            logger.DEBUG(f'Article {pmid} Cite Crawler Deep = {article.CiteCrawlerDeep}.'  , deep = 5)
    return article

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


    refresh_point = 0
    for id in l_pmid:
        try:
            number_of_article_move_forward = number_of_article_move_forward + 1
            
            if refresh_point == 5:
                refresh_point = 0
                refresh()
                logger.INFO(f'There are {str(total_article_in_current_state - number_of_article_move_forward)} article(s) left ', forecolore='yellow')
                min = (total_article_in_current_state - number_of_article_move_forward) / 60
                logger.INFO(f'It takes at least {str(int(min))} minutes or {str(int(min/60))} hours', forecolore='yellow')
            else:
                refresh_point = refresh_point + 1

            a = get_article_by_pmid(id)
            try:
                updated_article = Article(**a.copy())
            except:
                # print(a.__dict__)
                print(type(a))
                backward_dict = a.copy()
                backward = Article()
                backward.PMID = backward_dict['PMID']
                backward.State = 0
                updated_article = backward
                l = update_article_by_pmid(updated_article , updated_article.PMID)

            try:
                current_state = updated_article.State
            except:
                current_state = 0
            logger.DEBUG('Article ' + updated_article.PMID + ' with state ' + str(current_state) + ' forward to ' + str(current_state + 1))

            ## for re run
            # if current_state == 2 : current_state = 1

            if current_state is None:
                updated_article = _expand_details(updated_article)
                l = update_article_by_pmid(updated_article , updated_article.PMID)

            elif current_state == 0: # get article details from pubmed
                updated_article = _expand_details(updated_article)
                l = update_article_by_pmid(updated_article , updated_article.PMID)
                    
            elif current_state == 1: # Extract Data
                updated_article = _parsing_details(updated_article)
                l = update_article_by_pmid(updated_article , updated_article.PMID)
                if len(l) == 1:
                    pass
                else:
                    logger.ERROR('Duplication has Occurred')

            elif current_state == 2: # NER Title 
                updated_article = _ner_title(updated_article)
                l = update_article_by_pmid(updated_article , updated_article.PMID)
                # think after
                # if len(l) == 1:
                #     pass
                # else:
                #     logger.ERROR('Duplication has Occurred')

            elif current_state == 3: # Get Citation
                updated_article = _get_citation(updated_article)
                l = update_article_by_pmid(updated_article , updated_article.PMID)
                # think after
                # if len(l) == 1:
                #     pass
                # else:
                #     logger.ERROR('Duplication has Occurred')


            elif current_state == 4: # Create Knowledge
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
            elif current_state == 2: 
                raise
                updated_article = Article(**a.copy())  
                updated_article.State = -2
                update_article_by_pmid(updated_article , updated_article.PMID)
                refresh()
                exc_type, exc_value, exc_tb = sys.exc_info()
                logger.ERROR(f'Error {exc_type}')
                logger.ERROR(f'Error {exc_value}')

            else:
                refresh()
                raise


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

    move_state_forward(2)
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








        




    

   
