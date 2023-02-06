# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=("Electronic+Health+Records"[Mesh])+AND+("National"[Title/Abstract])&retmode=json&retstart=${esearchresultRetstart}&retmax=10000

# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=${PMID.0}&retmode=xml
import json
import time
import requests
import tinydb
import xmltodict


# from config.settings import ROOT,SETTINGS
from triplea.config.settings import ROOT,SETTINGS
from triplea.schemas.article import Article
from triplea.service.persist import create_article, get_article_by_state, update_article_by_pmid

def get_article_list():
    # api-endpoint
    URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?"
    
    # location given here
    location = "delhi technological university"
    
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'db': 'pubmed',
            'term': 'ehr' , 
            'retmode':'json' ,
            'retstart': 40,
            'retmax' : 20,
            }
    # sending get request and saving the response as response object
    r = requests.get(url = URL, params = PARAMS)

    # extracting data in json format
    data = r.json()
    data1= json.dumps(r.json(), indent=4)
    with open("sample.json", "w") as outfile:
        outfile.write(data1)

    print(data1)

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
        print(data_dict)
        return data_dict
    else:
        raise Exception('Error')
    


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

if __name__ == '__main__':
    # main()

    # data = get_article_details('36702245')
    # json_data = json.dumps(data)
    # with open("data.json", "w") as json_file:
    #     json_file.write(json_data)

    la = get_article_by_state(None)
    for a in la:
        # print(type(a))
        # print(a.__dict__)
        # print(a.copy())
        a = Article(**a.copy()) 
        try:
            status = a.State
        except:
            status = 0

    
        if status is None:
            # oa = get_article_details(a.PMID)
            # a.OreginalArticle = oa
            # a.State = 0
            # time.sleep(3)
            # l = update_article_by_pmid(a , a.PMID)
            # print(l)

            pass
        elif status == 0:
            # oa = get_article_details(a.PMID)
            # a.OreginalArticle = oa
            # a.State = 1
            # l = update_article_by_pmid(a , a.PMID)
            # time.sleep(3)
            pass
        elif status == 1: # Extract Data
            data = a.OreginalArticle
            data = data['PubmedArticleSet']['PubmedArticle']['PubmedData']
            
            ArticleId = data['ArticleIdList']['ArticleId']
            print(ArticleId)

            a.Title =  data['MedlineCitation']['Article']['ArticleTitle']
            pass
        else:
            pass

    print(type(a))
    