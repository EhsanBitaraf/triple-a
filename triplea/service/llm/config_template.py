# How to suppress OpenAI API warnings in Python
# https://stackoverflow.com/questions/71893613/how-to-suppress-openai-api-warnings-in-python
import logging
import os
import json
from triplea.config.settings import SETTINGS
from triplea.service.click_logger import logger

logging.getLogger().setLevel(logging.CRITICAL)


def read_llm_template():
    if os.path.exists(SETTINGS.AAA_LLM_TEMPLATE_FILE) is False:
        # raise FileNotFoundError(f"File {SETTINGS.AAA_LLM_TEMPLATE_FILE} Not Found.")
        logger.WARNING("LLM template not found or not configured.")
        return None

    with open(SETTINGS.AAA_LLM_TEMPLATE_FILE, encoding="utf-8") as f:
        d = json.load(f)
    return d
