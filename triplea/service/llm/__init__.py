

import json
import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

from triplea.utils.general import print_error

import warnings
warnings.filterwarnings("ignore", module="langchain_openai")

import os
import time
import sys
from typing import Any

# ChatOpenAI (same as you used before)
from langchain_openai import ChatOpenAI

# Backwards-compatible import for PromptTemplate:
# Try the new location first (langchain_core), then fall back to the old one (langchain).
try:
    # Newer LangChain versions use langchain_core.prompts
    from langchain_core.prompts import PromptTemplate
except Exception:
    # Older LangChain versions use langchain.prompts
    from langchain.prompts import PromptTemplate


import triplea.service.repository.persist as PERSIST

from triplea.service.llm.config_template import read_llm_template as template
from triplea.service.llm.config_template import read_llm_template_from_file

# Ensure an API key exists in the environment (keeps tests/local runs working)
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "dummy_api_key"

# Read template configuration once initially (functions re-read when needed)
T = template()

if T is not None:
    # Initialize the global LLM object from the config template
    GOLOBAL_LLM = ChatOpenAI(
        model_name=T["model_name"],
        temperature=T["temperature"],
        openai_api_base=T["base_path"],
        frequency_penalty=T["frequency_penalty"],
        presence_penalty=T["presence_penalty"],
        max_tokens=T["max_tokens"],
        top_p=T["top_p"],
    )
    logger.debug(f"Run LLM from {T['base_path']} model : {T['model_name']}")


def get_prompt_with_template(title: str, abstract: str):
    """
    Build a prompt string using the globally loaded template T.
    """
    prompt_template = PromptTemplate.from_template(T["template"])
    prompt = prompt_template.format(title=title, abstract=abstract)
    return prompt


def get_prompt_with_template_from_special_template_file(template_file, dbuid: str):
    """
    Read a template from a file and build a prompt for an article identified by dbuid.
    """
    T_local = read_llm_template_from_file(template_file)
    prompt_template = PromptTemplate.from_template(T_local["template"])
    a = PERSIST.get_article_by_id(dbuid)
    prompt = prompt_template.format(title=a['Title'], abstract=a['Abstract'])
    return prompt


def extract_text_from_response(response: Any) -> str:
    """
    Normalize different possible response shapes and return a plain text string.
    Handles:
      - response.content (string)
      - response.text (string)
      - response.generations -> nested lists of Generation objects
      - response.data dicts or lists
      - plain string responses
      - dict/list responses (fallback to JSON string)
    Returns an empty string if no usable text is found.
    """
    try:
        # 1) Direct `content` attribute (used in your original code)
        if hasattr(response, "content") and isinstance(response.content, str):
            return response.content

        # 2) Direct `text` attribute
        if hasattr(response, "text") and isinstance(response.text, str):
            return response.text

        # 3) `generations` structure (common in some LangChain versions)
        if hasattr(response, "generations"):
            gens = response.generations
            if isinstance(gens, list) and len(gens) > 0:
                first = gens[0]
                # If nested list: List[List[Generation]]
                if isinstance(first, list) and len(first) > 0:
                    gen0 = first[0]
                    if hasattr(gen0, "text"):
                        return gen0.text
                    return str(gen0)
                # If flat list and elements have .text
                if hasattr(first, "text"):
                    return first.text
                return str(first)

        # 4) `data` attribute (some integrations)
        if hasattr(response, "data"):
            d = response.data
            if isinstance(d, dict):
                for k in ("text", "content", "output_text", "message"):
                    if k in d and isinstance(d[k], str):
                        return d[k]
                # Fallback to JSON dump
                return json.dumps(d)
            else:
                return str(d)

        # 5) If the response is already a plain string
        if isinstance(response, str):
            return response

        # 6) If the response is a dict or list, try to find a reasonable text key
        if isinstance(response, (dict, list)):
            if isinstance(response, dict):
                for k in ("content", "text", "output", "message"):
                    if k in response and isinstance(response[k], str):
                        return response[k]
            return json.dumps(response)

        # Final fallback to str()
        return str(response)
    except Exception:
        # In case of unexpected errors, return an empty string to allow upstream handling
        return ""


def call_llm_and_get_text(llm: Any, prompt: str) -> str:
    """
    Try several call patterns to support multiple LangChain versions and wrappers:
      1) llm.invoke(input=prompt)
      2) llm.predict(prompt)
      3) llm(prompt)  (callable)
      4) llm.generate([prompt])
    The function returns the extracted text or an empty string if none of the call patterns produced text.
    """
    # 1) try invoke (preferred on some newer langchain_openai wrappers)
    try:
        if hasattr(llm, "invoke"):
            resp = llm.invoke(input=prompt)
            text = extract_text_from_response(resp)
            if text:
                return text
    except Exception:
        logger.debug("llm.invoke failed or returned no usable text", exc_info=True)

    # 2) try predict (older pattern)
    try:
        if hasattr(llm, "predict"):
            text = llm.predict(prompt)
            if isinstance(text, str) and text:
                return text
    except Exception:
        logger.debug("llm.predict failed", exc_info=True)

    # 3) try calling the LLM object directly (some wrappers implement __call__)
    try:
        if callable(llm):
            out = llm(prompt)
            if isinstance(out, str) and out:
                return out
            text = extract_text_from_response(out)
            if text:
                return text
    except Exception:
        logger.debug("callable llm(...) failed", exc_info=True)

    # 4) try generate (returns structured object in some versions)
    try:
        if hasattr(llm, "generate"):
            gen = llm.generate([prompt])
            text = extract_text_from_response(gen)
            if text:
                return text
    except Exception:
        logger.debug("llm.generate failed", exc_info=True)

    # If nothing worked, return an empty string
    return ""


def question_with_template_for_llm(title: str, abstract: str):
    """
    Main function to build the prompt from template, call the LLM, and package the result.
    Reads the template configuration on each call to support dynamic changes like stop_immediately.
    """
    T_local = template()  # read config each call (for stop_immediately etc.)

    if T_local.get("stop_immediately") == 1:
        # Immediate stop requested by config; exit the process
        print()
        logger.info("Stop immediately.")
        sys.exit()

    prompt_template = PromptTemplate.from_template(T_local["template"])
    llm = GOLOBAL_LLM
    prompt = prompt_template.format(title=title, abstract=abstract)

    # Basic check for malformed template
    if "}}" in prompt:
        raise Exception("Malformed template (found '}}').")

    # Very rough token approximation using whitespace splitting
    input_tokens = len(prompt.split())

    start = time.time()
    text = call_llm_and_get_text(llm, prompt)
    end = time.time()

    output_tokens = len(text.split()) if text else 0

    if text == "":
        raise Exception("response content is empty!")

    r = {
        "TemplateID": T_local.get("model_template_id"),
        "InputTokens": input_tokens,
        "OutputTokens": output_tokens,
        "TimeTaken": (end - start),
    }

    if T_local.get("response_must_be_json"):
        # Normalize newlines and try to parse JSON
        text_single_line = text.replace("\n", " ")
        try:
            r["Response"] = json.loads(text_single_line)
        except Exception as e:
            r["Response"] = {"StringContent": text_single_line}
            if isinstance(e, json.JSONDecodeError):
                r["Response"]["ErrorMsg"] = e.msg
                r["Response"]["colno"] = e.colno
            else:
                r["Response"]["ErrorType"] = str(type(e))
            print_error()
    else:
        r["Response"] = text

    return r
