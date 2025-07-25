# How to suppress OpenAI API warnings in Python
# https://stackoverflow.com/questions/71893613/how-to-suppress-openai-api-warnings-in-python
import json
import logging

from triplea.utils.general import print_error

logging.getLogger().setLevel(logging.CRITICAL)

import os
import time
from triplea.service.click_logger import logger
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import triplea.service.repository.persist as PERSIST

from triplea.service.llm.config_template import read_llm_template as template
from triplea.service.llm.config_template import read_llm_template_from_file

os.environ["OPENAI_API_KEY"] = "dummy_key"

T = template()

if T is not None:
    GOLOBAL_LLM = ChatOpenAI(
        model_name=T["model_name"],
        temperature=T["temperature"],
        openai_api_base=T["base_path"],
        frequency_penalty=T["frequency_penalty"],
        presence_penalty=T["presence_penalty"],
        max_tokens=T["max_tokens"],
        top_p=T["top_p"],
        # top_k=0,
    )

    # # Simple Load
    # GOLOBAL_LLM = ChatOpenAI(model_name=model_name, temperature=temperature, openai_api_base=base_path)
    logger.DEBUG(f"Run LLM from {T['base_path']} model : {T['model_name']}")


def get_prompt_with_template(title: str, abstract: str):
    prompt_template = PromptTemplate.from_template(T["template"])
    prompt = prompt_template.format(title=title, abstract=abstract)
    return prompt

# Insert from dt-main-lab.ipynb for new version
def get_prompt_with_template_from_special_template_file(template_file, dbuid: str):
    T = read_llm_template_from_file(template_file)
    prompt_template = PromptTemplate.from_template(T["template"])
    a = PERSIST.get_article_by_id(dbuid)
    prompt = prompt_template.format(title=a['Title'], abstract=a['Abstract'])
    print(f"""Title with DBUID {dbuid}: {a['Title']} """)
    return prompt


def question_with_template_for_llm(title: str, abstract: str):
    T = template()  # I read this on every call for field stop_immediately

    if T["stop_immediately"] == 1:
        print()
        logger.INFO("Stop immediately.")
        # return
        exit()

    prompt_template = PromptTemplate.from_template(T["template"])

    # Load LLM
    llm = GOLOBAL_LLM

    prompt = prompt_template.format(title=title, abstract=abstract)

    if str.__contains__(prompt, "}}"):
        raise Exception("chera")
    # # For Development Mode
    # print()
    # print(prompt)
    # print()

    # Calculate input tokens
    input_tokens = len(prompt.split(" "))

    start = time.time()
    response = llm.invoke(input=prompt)
    end = time.time()

    # Calculate output tokens
    output_tokens = len(response.content.split(" "))

    if response.content == "":
        raise Exception("response.content is empty!")

    r = {
        "TemplateID": T["model_template_id"],
        "InputTokens": input_tokens,
        "OutputTokens": output_tokens,
        "TimeTaken": (end - start),
    }
    if T["response_must_be_json"]:
        if isinstance(response.content, dict):
            raise Exception("Nabilam")
        response.content = str.replace(response.content, "\n", " ")
        # response.content = str.replace(response.content, '\"', "'")
        try:
            r["Response"] = json.loads(response.content)
            # r["Response"] = json.loads(json.dumps(response.content))
        except Exception as e:
            # Error in convert str to json
            r["Response"] = {"StringContent": response.content}
            if isinstance(e, json.JSONDecodeError):
                r["Response"]["ErrorMsg"] = e.msg
                r["Response"]["colno"] = e.colno
            else:
                r["Response"]["ErrorType"] = str(type(e))

            print_error()

    return r


