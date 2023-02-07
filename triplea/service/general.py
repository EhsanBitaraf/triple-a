# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=("Electronic+Health+Records"[Mesh])+AND+("National"[Title/Abstract])&retmode=json&retstart=${esearchresultRetstart}&retmax=10000

# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=${PMID.0}&retmode=xml
import json
import time
from typing import Optional
import requests
import tinydb
import xmltodict
import click


from triplea.service.click_logger import logger
# from config.settings import ROOT,SETTINGS
from triplea.config.settings import ROOT,SETTINGS
from triplea.schemas.article import Article
from triplea.service.persist import create_article, get_all_article_count, get_article_by_state, insert_new_pmid, update_article_by_pmid

def get_article_list(retstart:int, retmax:int, search_term:str)-> dict:
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

def get_article_details(PMID):
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
    data = get_article_list(0 ,1 , searchterm)
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
        chunkdata = get_article_list(start , retmax ,searchterm)
        save_article_pmid_list_in_kgrep(chunkdata)

    # for last round
    start = ((i + 1) * retmax) - retmax
    mid = total - (retmax * round)
    logger.INFO('Round (' + str(i+1) + ') : ' + 'Get another ' + str(mid) + ' record (total ' + str(total) + ' record)', deep = 13)
    chunkdata = get_article_list(start , retmax ,searchterm)
    save_article_pmid_list_in_kgrep(chunkdata)

def move_state_forward(state: int):
    la = get_article_by_state(state)
    for a in la:
        a = Article(**a.copy()) 
        
        try:
            status = a.State
        except:
            status = 0
        logger.DEBUG('Article ' + a.PMID + ' with state ' + str(status) + ' forward to ' + str(status + 1))

        if status is None:
            oa = get_article_details(a.PMID)
            a.OreginalArticle = oa
            a.State = 0
            time.sleep(3)
            l = update_article_by_pmid(a , a.PMID)
            print(l)

            pass
        elif status == 0:
            oa = get_article_details(a.PMID)
            a.OreginalArticle = oa
            a.State = 1
            l = update_article_by_pmid(a , a.PMID)
            time.sleep(3)
        
        elif status == 1: # Extract Data
            data = a.OreginalArticle
            PubmedData = data['PubmedArticleSet']['PubmedArticle']['PubmedData']
            
            ArticleId = PubmedData['ArticleIdList']['ArticleId']
            for a_id in ArticleId:
                if a_id['@IdType'] == 'doi':
                    a.DOI = a_id['#text']
            
            pubmed_article_data = data['PubmedArticleSet']['PubmedArticle']['MedlineCitation']['Article']
            a.Title =  pubmed_article_data['ArticleTitle']
            a.Journal = pubmed_article_data['Journal']['Title']
            a.Abstract = pubmed_article_data['Abstract']
            pass
        else:
            pass

if __name__ == '__main__':
    logger.WARNING('Number of article in knowlege repository is ' + str(get_all_article_count()))
    move_state_forward(1)
    # click.echo(click.style('Number of article in knowlege repository is ', fg='green') + ' ' + click.style(str(get_all_article_count()), fg='red'))
    # click.secho('Hello World!', fg='green')
    # click.secho('Some more text', bg='blue', fg='white')
    # click.secho('ATTENTION', blink=True, bold=True)

    

    

   







    




    