from triplea.config.settings import SETTINGS
import requests
import xmltodict
import json
from triplea.service.click_logger import logger


def get_article_list_from_arxiv(search_query: str, start: int, max_results: int) -> dict:
    URL = "http://export.arxiv.org/api/query?"

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {
        "search_query": search_query, 
        "start": start,  
        "max_results": max_results,
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

    # Convert XML to Json
    if r.status_code == 200:
        xml = r.content
        data_dict = xmltodict.parse(xml)
        return data_dict
    else:
        raise Exception(f"Error HTTP : {r.status_code}")
    