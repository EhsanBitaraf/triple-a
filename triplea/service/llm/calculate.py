# from triplea.db.mongo_nav import get_article_title_and_abstract
from triplea.schemas.article import Article
from triplea.service.llm import get_prompt_with_template
import triplea.service.repository.persist as PERSIST
from triplea.utils.general import print_error
from triplea.service.click_logger import logger
import click


def precalculate(
    time_taken_per_request: float, avarage_output_tokens: int, proccess_bar=True
):
    # Tis not General
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
            print(logger.ERROR(f"Error in parsing article. ID = {id}"))
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
