from datetime import datetime
import json
import sys
import traceback
from triplea.schemas.article import Article
from triplea.service.click_logger import logger
from bson import ObjectId


def get_tqdm():
    try:
        # Check if running in IPython (Jupyter or IPython shell)
        from IPython import get_ipython
        shell = get_ipython()
        if shell and 'IPKernelApp' in shell.config:
            from tqdm.notebook import tqdm
        else:
            from tqdm import tqdm
    except:
        # Fallback if IPython isn't available
        from tqdm import tqdm
    return tqdm


def safe_csv(text):
    if isinstance(text, int):
        return text
    elif isinstance(text, float):
        return text

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
    logger.ERROR(f"line : {exc_tb.tb_lineno}")
    traceback.print_tb(exc_tb)  # In debug mode


def print_pretty_dict(d: dict):
    json_formatted_str = json.dumps(d, indent=2)
    print(json_formatted_str)


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Article):
            # Serialize the Article object to a dictionary
            return obj.dict()
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)
