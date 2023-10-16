from triplea.config.settings import SETTINGS
import requests
import xmltodict
import json
from triplea.service.click_logger import logger


def get_article_list_from_pubmed(retstart: int, retmax: int, search_term: str) -> dict:
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
    PARAMS = {
        "db": "pubmed",  # https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch
        "term": search_term,  # Entrez text query. All special characters must be URL encoded. Spaces may be replaced by '+' signs. For very long queries (more than several hundred characters long), consider using an HTTP POST call. See the PubMed or Entrez help for information about search field descriptions and tags. Search fields and tags are database specific.
        "retmode": "json",  # Retrieval type. Determines the format of the returned output. The default value is ‘xml’ for ESearch XML, but ‘json’ is also supported to return output in JSON format.
        "retstart": retstart,  # Sequential index of the first UID in the retrieved set to be shown in the XML output (default=0, corresponding to the first record of the entire set). This parameter can be used in conjunction with retmax to download an arbitrary subset of UIDs retrieved from a search.
        "retmax": retmax,  # Total number of UIDs from the retrieved set to be shown in the XML output (default=20). By default, ESearch only includes the first 20 UIDs retrieved in the XML output. If usehistory is set to 'y', the remainder of the retrieved set will be stored on the History server; otherwise these UIDs are lost. Increasing retmax allows more of the retrieved UIDs to be included in the XML output, up to a maximum of 10,000 records.
        # # For chunking data when more than 10000
        # "datetype" : "pdat",
        # "mindate" : "2021/01/01",
        # "maxdate" : "2023/09/17"
    }

    headers = {"User-Agent": SETTINGS.AAA_CLIENT_AGENT}

    # To use HTTP Basic Auth with your proxy, use the http://user:password@host.com/ syntax:
    if SETTINGS.AAA_PROXY_HTTP is not None:
        proxy_servers = {
            "http": SETTINGS.AAA_PROXY_HTTP,
            "https": SETTINGS.AAA_PROXY_HTTPS,
        }
    else:
        proxy_servers = None

    # sending get request and saving the response as response object
    try:
        r = requests.get(url=URL, params=PARAMS, headers=headers, proxies=proxy_servers)
    except Exception:
        raise Exception("Connection Error.")

    # extracting data in json format
    try:
        data = r.json()
    except Exception as ex:
        logger.ERROR(f"Error : {ex}")
        logger.ERROR(f"{type(r)}  {r} ")
        raise
    return data


def get_article_details_from_pubmed(PMID) -> dict:
    """
    It takes a PMID as input and returns a dictionary of the article's details from Pubmed

    :param PMID: The PubMed ID of the article you want to get the details of
    :return: It returns a dictionary that is converted from the [XML output](https://www.nlm.nih.gov/bsd/licensee/elements_descriptions.html) of the pubmed site to the json model
    """
    URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?"
    PARAMS = {
        "db": "pubmed",
        "id": PMID,
        "retmode": "xml",
    }

    headers = {"User-Agent": SETTINGS.AAA_CLIENT_AGENT}

    # To use HTTP Basic Auth with your proxy, use the http://user:password@host.com/ syntax:
    if SETTINGS.AAA_PROXY_HTTP is not None:
        proxy_servers = {
            "http": SETTINGS.AAA_PROXY_HTTP,
            "https": SETTINGS.AAA_PROXY_HTTPS,
        }
    else:
        proxy_servers = None

    r = requests.get(url=URL, params=PARAMS, headers=headers, proxies=proxy_servers)
    if r.status_code == 200:
        xml = r.content
        data_dict = xmltodict.parse(xml)
        return data_dict
    else:
        raise Exception("Error")


def get_cited_article_from_pubmed(PMID) -> dict:
    URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?"
    PARAMS = {
        "dbfrom": "pubmed",
        "db": "pubmed",
        "id": PMID,
        "retmode": "json",
    }

    headers = {"User-Agent": SETTINGS.AAA_CLIENT_AGENT}

    # To use HTTP Basic Auth with your proxy, use the http://user:password@host.com/ syntax:
    if SETTINGS.AAA_PROXY_HTTP is not None:
        proxy_servers = {
            "http": SETTINGS.AAA_PROXY_HTTP,
            "https": SETTINGS.AAA_PROXY_HTTPS,
        }
    else:
        proxy_servers = None

    r = requests.get(url=URL, params=PARAMS, headers=headers, proxies=proxy_servers)
    if r.status_code == 200:
        # xml = r.content
        # data_dict = xmltodict.parse(xml)
        data_byte = r.content  # it is byte

        data = json.loads(data_byte.decode("utf-8"))
        if "linksets" in data:
            for link in data["linksets"]:
                # print(type(link))
                # print(type(link['linksetdbs']))
                for linkdb in link["linksetdbs"]:
                    rd = linkdb["linkname"]
                    if (
                        rd == "pubmed_pubmed"
                        or rd == "pubmed_pubmed_alsoviewed"
                        or rd == "pubmed_pubmed_combined"
                        or rd == "pubmed_pubmed_five"
                        or rd == "pubmed_pubmed_reviews"
                        or rd == "pubmed_pubmed_reviews_five"
                    ):
                        pass
                    else:
                        # print(linkdb['linkname'])
                        pass
                    if linkdb["linkname"] == "pubmed_pubmed_citedin":
                        return linkdb["links"]
        else:
            raise
    else:
        raise Exception("Error")
