# How to suppress OpenAI API warnings in Python
# https://stackoverflow.com/questions/71893613/how-to-suppress-openai-api-warnings-in-python
import logging
import os
import json
from triplea.config.settings import SETTINGS

logging.getLogger().setLevel(logging.CRITICAL)


def read_llm_template():
    # print(SETTINGS.AAA_LLM_TEMPLATE_FILE)
    if os.path.exists(SETTINGS.AAA_LLM_TEMPLATE_FILE) is False:
        raise FileNotFoundError

    with open(SETTINGS.AAA_LLM_TEMPLATE_FILE) as f:
        d = json.load(f)
    return d
