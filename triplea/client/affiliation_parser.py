from triplea.config.settings import SETTINGS
import requests
from triplea.service.click_logger import logger
from urllib.parse import quote

session = requests.Session()


def parse_affiliation(text: str) -> list:
    URL = f"{SETTINGS.AAA_TOPIC_EXTRACT_ENDPOINT}/affiliation"

    # # data to be sent to api
    # PARAMS = {
    #     "text": text,
    # }

    text_encode = quote(text)
    url = f"{URL}/{text_encode}"

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
        r = session.get(url=url, headers=headers, proxies=proxy_servers)

    except Exception:
        raise Exception("Connection Error.")

    # extracting data in json format
    try:
        if r.status_code == 200:
            data = r.json()
            if "status" in data:
                return data["result"]
            else:
                logger.ERROR("status not exist.")
                raise
        else:
            logger.ERROR(f"ERROR : {r.status_code}")
            logger.ERROR(f"Reason : {r.reason}")

    except Exception as ex:
        logger.ERROR(f"Error : {ex}")
        logger.ERROR(f"{type(r)}  {r} ")
        raise
