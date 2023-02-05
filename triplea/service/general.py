# https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=("Electronic+Health+Records"[Mesh])+AND+("National"[Title/Abstract])&retmode=json&retstart=${esearchresultRetstart}&retmax=10000


import json
import requests

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

def main():
    # Opening JSON file
    f = open('sample.json')
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    
    # Iterating through the json
    # list
    for i in data['esearchresult']['idlist']:
        print(i)
    
    # Closing file
    f.close()

if __name__ == '__main__':
    main()