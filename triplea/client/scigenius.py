from triplea.config.settings import SETTINGS
import requests
import json
from triplea.schemas.article import Article
# from triplea.utils.general import JSONEncoder
from triplea.utils.general import print_error


session = requests.Session()


def article_embedding(article: Article) -> bool:
    URL = f"{SETTINGS.AAA_SCIGENIUS_ENDPOINT}/embedding/"

    # data to be sent to api
    # data = {
    #     "Text": text.replace("\n", " "),
    #     "Method": method,
    #     "Top": top,
    #     "Threshold": threshold,
    # }
    data = article

    headers = {
        "User-Agent": SETTINGS.AAA_CLIENT_AGENT,
    }

    # To use HTTP Basic Auth with your proxy,
    #  use the http://user:password@host.com/ syntax:
    if SETTINGS.AAA_PROXY_HTTP is not None:
        proxy_servers = {
            "http": SETTINGS.AAA_PROXY_HTTP,
            "https": SETTINGS.AAA_PROXY_HTTPS,
        }
    else:
        proxy_servers = None

    # sending get request and saving the response as response object
    try:
        # j_data = json.dumps(data)
        # j_data = json.loads(
        #     json.dumps(article, cls=JSONEncoder, sort_keys=True, indent=4)
        # )
        # j_data= article.dict()

        j_data = {
            "SourceBank": article.SourceBank,
            "Title": article.Title.replace("\n", " "),
            "Abstract": article.Abstract,
            "ArxivID": article.ArxivID,
        }
        j_data = json.dumps(j_data)
        j_data = j_data.replace("\n", " ")
        # print()
        # print(j_data)
        r = session.post(url=URL, data=j_data, headers=headers, proxies=proxy_servers)
    except Exception:
        print_error()
        raise Exception("Connection Error.")

    if r.status_code != 201:
        raise Exception(f"HTTP Error {r.status_code}")

    # extracting data in json format
    try:
        data = r.json()
        if "Status" in data:
            if data["Status"] == "Ok":
                return True
            else:
                raise Exception("status not Ok.")
        else:
            raise Exception("status not exist.")

    except Exception as ex:
        # logger.ERROR(f"Error : {ex}")
        # logger.ERROR(f"{type(r)}  {r} ")
        raise ex
