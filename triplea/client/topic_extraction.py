from triplea.config.settings import SETTINGS
import requests
import json
from triplea.service.click_logger import logger

# https://stackoverflow.com/questions/62599036/python-requests-is-slow-and-takes-very-long-to-complete-http-or-https-request
session = requests.Session()

# import httpx
# async def extract_topic(text: str,
#                    method: str,
#                    top:int=10,
#                    threshold:float=0) -> list:


#     URL  = SETTINGS.AAA_TOPIC_EXTRACT_ENDPOINT


#     # data to be sent to api
#     data = {
#             "Text": text.replace("\n"," "),
#             "Method": method,
#             "Top": top,
#             "Threshold": threshold
#             }

#     headers = {
#         "User-Agent": SETTINGS.AAA_CLIENT_AGENT,
#     }

#     # To use HTTP Basic Auth with your proxy,
#     #  use the http://user:password@host.com/ syntax:
#     if SETTINGS.AAA_PROXY_HTTP is not None:
#         proxy_servers = {
#             "http": SETTINGS.AAA_PROXY_HTTP,
#             "https": SETTINGS.AAA_PROXY_HTTPS,
#         }
#     else:
#         proxy_servers = None

#     # # sending get request and saving the response as response object
#     # try:
#     #     r = requests.post(url=URL,
#     #                     data=json.dumps(data),
#     #                     headers=headers,
#     #                     proxies=proxy_servers)
#     # except Exception:
#     #     raise Exception("Connection Error.")


# async with httpx.AsyncClient() as client:
#     response = await client.post(url=URL,
#                     data=json.dumps(data),
#                     headers=headers,
#                     proxies=proxy_servers)
#     response.raise_for_status()

#     data =  response.json()
#     if 'status' in data:
#         return data['r']
#     else:
#         logger.ERROR('status not exist.')
#         raise

# # extracting data in json format
# try:
#     data = r.json()
#     if 'status' in data:
#         return data['r']
#     else:
#         logger.ERROR('status not exist.')
#         raise

# except Exception as ex:
#     logger.ERROR(f"Error : {ex}")
#     logger.ERROR(f"{type(r)}  {r} ")
#     raise


def extract_topic(text: str, method: str, top: int = 10, threshold: float = 0) -> list:
    URL = f"{SETTINGS.AAA_TOPIC_EXTRACT_ENDPOINT}/topic"

    # data to be sent to api
    data = {
        "Text": text.replace("\n", " "),
        "Method": method,
        "Top": top,
        "Threshold": threshold,
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
        j_data = json.dumps(data)
        r = session.post(url=URL, data=j_data, headers=headers, proxies=proxy_servers)

    except Exception:
        raise Exception("Connection Error.")

    # extracting data in json format
    try:
        data = r.json()
        if "status" in data:
            return data["r"]
        else:
            logger.ERROR("status not exist.")
            raise

    except Exception as ex:
        logger.ERROR(f"Error : {ex}")
        logger.ERROR(f"{type(r)}  {r} ")
        raise
