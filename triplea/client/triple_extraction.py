from triplea.config.settings import SETTINGS
import requests
import json
from triplea.service.click_logger import logger

session = requests.Session()


def extract_triple(text: str) -> list:
    URL = SETTINGS.AAA_TOPIC_EXTRACT_ENDPOINT + "/triple/"

    # data to be sent to api
    data = {
        "text": text.replace("\n", " "),
    }

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
        r = session.post(
            url=URL, data=json.dumps(data), headers=headers, proxies=proxy_servers
        )
    except Exception:
        raise Exception("Connection Error.")

    if r.status_code != 201:
        raise Exception(f"HTTP Error {r.status_code}")

    # extracting data in json format
    try:
        data = r.json()
        if "status" in data:
            return data["result"]
        else:
            # logger.ERROR("status not exist.")
            raise Exception("status not exist.")

    except Exception as ex:
        logger.ERROR(f"Error : {ex}")
        logger.ERROR(f"{type(r)}  {r} ")
        raise
