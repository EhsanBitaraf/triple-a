# flake8: noqa
# Depreciate
import os
import time
from triplea.service.click_logger import logger
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load Template
import triplea.service.llm.model_template_101 as MODEL

# How to suppress OpenAI API warnings in Python
# https://stackoverflow.com/questions/71893613/how-to-suppress-openai-api-warnings-in-python
import logging

logging.getLogger().setLevel(logging.CRITICAL)


os.environ["OPENAI_API_KEY"] = "dummy_key"

# base_path="http://ai-api1.lab-ai.ir/v1"
# base_path="http://172.16.20.47:8465"
# model_name="mistral-7b-openorca.Q6_K.gguf"

# # Docker llama2
# base_path="http://172.16.20.47:7185/v1"
# model_name="llama2-chat"

# # DeepInfra
# base_path="https://api.deepinfra.com/v1/openai"
# model_name= "mistralai/Mistral-7B-Instruct-v0.1"
# os.environ['OPENAI_API_KEY'] = 'ig91NvF8DIeWZDjEFuXcHUU8rYqV48UC'

# # oobabooga
# base_path="http://localhost:5003/v1"
# model_name= "openbuddy-llama2-70B-v13.2-AWQ"
os.environ["OPENAI_API_KEY"] = "dummy_key"

# base_path=SETTINGS.SCIG_LLM_API_BASE
# model_name=SETTINGS.SCIG_LLM_MODEL_NAME

# base on Template
base_path = MODEL.base_path
model_name = MODEL.model_name


def get_llm(temperature: float):
    llm = ChatOpenAI(
        model_name=model_name,
        temperature=temperature,
        openai_api_base=base_path,
        frequency_penalty=MODEL.frequency_penalty,
        presence_penalty=MODEL.presence_penalty,
        max_tokens=MODEL.max_tokens,
        top_p=MODEL.top_p,
        #   top_k=0,
    )

    # llm = ChatOpenAI(model_name=model_name,
    #                  temperature=temperature,
    #                  openai_api_base=base_path)
    logger.DEBUG(f"Run LLM from {base_path} model : {model_name}")
    return llm


GOLOBAL_LLM = get_llm(MODEL.temperature)


def sample0():
    # Define the prompt template
    template = """Question: {question} Answer: Let's think step by step."""
    prompt = PromptTemplate(template=template, input_variables=["question"])

    # Initialize the LLM and prompt
    llm = get_llm(0.6)
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    # Provide a question and run the LLM chain
    question = "When was Novak Djokovic born?"
    print(llm_chain.run(question))


def sample1():
    prompt_template = PromptTemplate.from_template(
        template="Write a {length} story about: {content}"
    )

    llm = get_llm(0.6)

    prompt = prompt_template.format(
        length="2-sentence",
        content="The hometown of the legendary data scientist, Harpreet Sahota",
    )

    print(prompt)
    print()
    # response = llm.predict(
    #     text=prompt
    # )
    response = llm.invoke(input=prompt)
    print(type(response))
    print(response.content)


def sample_check_topic(title: str, abstract: str):
    # prompt_template = PromptTemplate.from_template(
    #     template='''Check out the article with title "{title}" and below abstract then determined this is related to the Large Language Model(LLM) assessment or evaluation? Just answer only yes or no
    #     abstract : {abstract}
    #     '''
    # )

    prompt_template = PromptTemplate.from_template(
        template="""Check the title and abstract of the article below and tell me if this article has anything to do with LLMs (Large Language Models) assessment methods? Your answer must be yes or no.
title: {title}
abstract : {abstract}
        """
    )

    # prompt_template = PromptTemplate.from_template(
    #     template='''Check out the article with title "{title}" and below abstract then determined the main topic of the article in two words.
    #     abstract : {abstract}
    #     '''
    # )

    llm = get_llm(0.7)

    prompt = prompt_template.format(title=title, abstract=abstract)

    print(prompt)
    input_tokens = len(prompt.split(" "))

    print()

    start = time.time()
    response = llm.invoke(input=prompt)
    end = time.time()

    output_tokens = len(response.content.split(" "))
    print(f"input tokens  : {input_tokens}")
    print(f"output tokens : {output_tokens}")
    print(f"Time : {end - start}")
    print(response.content)


def question_with_template_for_llm(title: str, abstract: str):
    prompt_template = PromptTemplate.from_template(
        template="""Check the title and abstract of the article below and tell me if this article has anything to do with LLMs (Large Language Models) assessment methods? Your answer must be yes or no.
title: {title}
abstract : {abstract}
        """  # noqa: E501
    )

    # Load LLM
    llm = GOLOBAL_LLM

    prompt = prompt_template.format(title=title, abstract=abstract)

    input_tokens = len(prompt.split(" "))

    start = time.time()
    response = llm.invoke(input=prompt)
    end = time.time()

    output_tokens = len(response.content.split(" "))

    return {
        "TemplateID": MODEL.model_template_id,
        "InputTokens": input_tokens,
        "OutputTokens": output_tokens,
        "TimeTaken": (end - start),
        "Response": response.content,
    }

    print(f"id : {MODEL.model_template_id}")
    print(f"input tokens  : {input_tokens}")
    print(f"output tokens : {output_tokens}")
    print(f"Time : {end - start}")
    print(response.content)
