import json
import sys
from triplea.service.click_logger import logger
from bson import ObjectId


def safe_csv(text: str) -> str:
    if text is None:
        return ""
    if text.__contains__(","):
        if text.__contains__('"'):
            text = text.replace('"', "'")
            text = f'"{text[:-1]}"'
        else:
            text = f'"{text[:-1]}"'

    return text


def print_error():
    exc_type, exc_value, exc_tb = sys.exc_info()
    print()
    logger.ERROR(f"Error {exc_type}")
    logger.ERROR(f"Error {exc_value}")  

                # exc_type, exc_value, exc_tb = sys.exc_info()
                # print()
                # print(exc_tb.tb_lineno)
                # print()
                # traceback.print_tb(exc_tb)
                # logger.ERROR(f"Error {exc_type}")
                # logger.ERROR(f"Error {exc_value}")
                # logger.ERROR(f"Error {exc_tb}")
    
            # exc_type, exc_value, exc_tb = sys.exc_info()
            # print()
            # print(f"line : {exc_tb.tb_lineno}")
            # print(f"PMID : {updated_article.PMID}")
            # logger.ERROR(f"Error {exc_type}")
            # logger.ERROR(f"Error {exc_value}")
            # traceback.print_tb(exc_tb)    

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)