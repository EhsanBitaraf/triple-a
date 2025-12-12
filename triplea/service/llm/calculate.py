# from triplea.db.mongo_nav import get_article_title_and_abstract
import warnings
from triplea.schemas.article import Article
from triplea.service.llm import get_prompt_with_template
import triplea.service.repository.persist as PERSIST
from triplea.utils.general import print_error
from triplea.service.click_logger import logger as click_log
import click

from triplea.utils.general import get_tqdm
import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def precalculate_llm_cost(
    time_taken_per_request: float,
    avarage_output_tokens: int,
    proccess_bar=True
):
    l_id = PERSIST.get_article_id_list_by_cstate(0, "FlagShortReviewByLLM")
    n = 0
    max_record = len(l_id)
    logger.info(f"{str(max_record)} Article(s) exist for precalculate LLM cost")
    if proccess_bar:
        tqdm = get_tqdm()
        bar = tqdm(total=max_record, desc="Processing ")

    input_token = 0
    for id in l_id:
        n = n + 1
        try:
            a = PERSIST.get_article_by_id(id)
            article = Article(**a.copy())

            prompt = get_prompt_with_template(article.Title, article.Abstract)
            input_token = input_token + (len(prompt) / 4)

            if proccess_bar:
                bar.set_description(f"""{n} Article(s) check""")
                bar.update(1)


        except Exception as e:
            logger.error(f"Error processing article {id} but move next : {e}" , exc_info=True)

    output_token = avarage_output_tokens * n

    models = [
    {"model": "GPT-4o" , "input" : 2.50 , "output" : 10},
    {"model": "GPT-4o mini" , "input" : 0.150 , "output" : 0.600},
    {"model": "GPT-4.1", "input": 2, "output": 8},
    {"model": "gpt-4.1-mini", "input": 0.4, "output": 1.6},
    {"model": "OpenAI o1" , "input" :15.00 , "output" : 60.00 },
    {"model": "OpenAI o3-mini" , "input" :1.10 , "output" : 4.40 },
    {"model": "GPT-5", "input": 1.25, "output": 10.00},
    {"model": "GPT-5 mini", "input": 0.25, "output": 2.00},
    {"model": "GPT-5 nano", "input": 0.05, "output": 0.40},
    
    ]

    total_time = time_taken_per_request * n
    logger.info(f"Input token = {input_token}, Estimation of output token = {output_token}, Estimate of Total Time = {total_time}")
    total= input_token + output_token
    
    r = []
    for m in models:
        model = m['model']
        input_price_per_million_tokens = m['input']
        output_price_per_million_tokens = m['output']

        input_cost = (input_token / 1000000) * input_price_per_million_tokens 
        output_cost = (output_token / 1000000) * output_price_per_million_tokens 
        total_cost = input_cost + output_cost
        logger.info(f"The total cost based on the {model} is {total_cost}$.")
        r.append ({"model": model , "total_cost": total_cost})

    bar.close()
    return r

def post_calculate(template_id: str, limit_sample=0, proccess_bar=True):
    l_id = PERSIST.get_article_id_list_by_cstate(1, "FlagShortReviewByLLM")
    total_input_tokens = 0
    total_output_tokens = 0
    total_time_taken = 0
    n = 0
    doc_number = 0
    if proccess_bar:
        bar = click.progressbar(length=len(l_id), show_pos=True, show_percent=True)
    for id in l_id:
        n = n + 1
        a = PERSIST.get_article_by_id(id)
        article = Article(**a.copy())

        for d in article.ReviewLLM:
            if template_id == "":  # Unlimited
                doc_number = doc_number + 1
                total_input_tokens = total_input_tokens + d["InputTokens"]
                total_output_tokens = total_output_tokens + d["OutputTokens"]
                total_time_taken = total_time_taken + d["TimeTaken"]
            else:
                if d["TemplateID"] == template_id:
                    doc_number = doc_number + 1
                    total_input_tokens = total_input_tokens + d["InputTokens"]
                    total_output_tokens = total_output_tokens + d["OutputTokens"]
                    total_time_taken = total_time_taken + d["TimeTaken"]

        # For View Proccess
        if proccess_bar:
            bar.label = f"""{n} Article(s) Calculate."""
            bar.update(1)

        if limit_sample != 0:  # Unlimited
            if n > limit_sample:
                break
    out = {}
    out["Document"] = doc_number
    out["TotalOutputTokens"] = total_output_tokens
    out["TotalInputTokens"] = total_input_tokens
    out["TotalTokens"] = total_input_tokens + total_output_tokens
    out["TotalTimeTaken"] = total_time_taken
    out["TokenPerSecond"] = out["TotalTokens"] / total_time_taken
    out["SecondPerRequest"] = total_time_taken / doc_number
    out["gCO2e"] = ((out["TotalTokens"]) / 1000) * 0.3
    # The input tokens for GPT-4 Turbo cost $0.01 per 1,000 tokens,
    # and the output tokens cost $0.03 per 1,000 tokens
    out["Price"] = ((total_input_tokens / 1000) * 0.01) + (
        (out["TotalOutputTokens"] / 1000) * 0.03
    )
    return out


def precalculate(
    time_taken_per_request: float, avarage_output_tokens: int, proccess_bar=True
):
    warnings.warn(
        """precalculate() is deprecated
          and will be removed in a future version.
          You can use precalculate_llm_cost""",
        DeprecationWarning,
        stacklevel=2
    )
    # This not General
    # artilce_list = get_article_title_and_abstract()

    l_id = PERSIST.get_article_id_list_by_cstate(0, "FlagShortReviewByLLM")

    total_input_tokens = 0
    n = 0
    doc_number = len(l_id)
    if doc_number == 0:
        return
    if proccess_bar:
        bar = click.progressbar(length=doc_number, show_pos=True, show_percent=True)
    for id in l_id:
        n = n + 1
        a = PERSIST.get_article_by_id(id)
        try:
            article = Article(**a.copy())
        except Exception:
            print()
            print(click_log.ERROR(f"Error in parsing article. ID = {id}"))
            print_error()

        prompt = get_prompt_with_template(article.Title, article.Abstract)

        # Calculate input tokens
        total_input_tokens = total_input_tokens + len(prompt.split(" "))

        if proccess_bar:
            bar.label = f"""{n} Article(s) Input Tokens are {total_input_tokens}."""
            bar.update(1)

    i = {}
    i["TotalInputTokens"] = total_input_tokens
    i["totalOutputTokens"] = doc_number * avarage_output_tokens
    total_tokens = total_input_tokens + i["totalOutputTokens"]
    total_time_taken = doc_number * time_taken_per_request
    token_per_second = total_tokens / total_time_taken
    i["TokenPerSecond"] = token_per_second
    i["SecondPerRequest"] = total_time_taken / doc_number
    i["gCO2e"] = ((total_tokens) / 1000) * 0.3
    # The input tokens for GPT-4 Turbo cost $0.01 per 1,000 tokens,
    # and the output tokens cost $0.03 per 1,000 tokens
    i["Price"] = ((total_input_tokens / 1000) * 0.01) + (
        (i["totalOutputTokens"] / 1000) * 0.03
    )

    return i
