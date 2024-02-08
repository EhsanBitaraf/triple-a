from triplea.config.settings import SETTINGS
import requests
import xmltodict
import json
from triplea.service.click_logger import logger


def get_article_list_from_arxiv(
    search_query: str, start: int, max_results: int
) -> dict:
    URL = "http://export.arxiv.org/api/query?"

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {
        "search_query": search_query,
        "start": start,
        "max_results": max_results,
    }

    headers = {"User-Agent": SETTINGS.AAA_CLIENT_AGENT}

    # To use HTTP Basic Auth with your proxy,
    # use the http://user:password@host.com/ syntax:
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


def get_pdf_by_arxiv_id(arxiv_id: str):
    URL = f"https://browse.arxiv.org/pdf/{arxiv_id}.pdf"

    headers = {"User-Agent": SETTINGS.AAA_CLIENT_AGENT}

    # To use HTTP Basic Auth with your proxy,
    # use the http://user:password@host.com/ syntax:
    if SETTINGS.AAA_PROXY_HTTP is not None:
        proxy_servers = {
            "http": SETTINGS.AAA_PROXY_HTTP,
            "https": SETTINGS.AAA_PROXY_HTTPS,
        }
    else:
        proxy_servers = None

    # sending get request and saving the response as response object
    try:
        r = requests.get(url=URL, headers=headers, proxies=proxy_servers)
    except Exception:
        raise Exception("Connection Error.")

    if r.status_code == 200:
        pdf = r.content
        print(type(pdf))
        return pdf
    else:
        raise Exception(f"Error HTTP : {r.status_code}")


# https://stackoverflow.com/questions/34503412/
#    download-and-save-pdf-file-with-python-requests-module
# http://requests.readthedocs.org/en/latest/user/
#    quickstart/#raw-response-content
# Chunking method
# url = 'http://www.hrecos.org//images/Data/forweb/HRTVBSH.Metadata.pdf'
# r = requests.get(url, stream=True)

# with open('/tmp/metadata.pdf', 'wb') as fd:
#     for chunk in r.iter_content(chunk_size):
#         fd.write(chunk)
