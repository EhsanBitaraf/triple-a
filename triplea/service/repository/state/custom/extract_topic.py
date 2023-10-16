import sys
from triplea.client.topic_extraction import extract_topic
from triplea.schemas.article import Article
from triplea.service.click_logger import logger

# from triplea.service.nlp.topic_extract import extract_textrank


def extract_topic_abstract(article: Article):
    article.FlagExtractTopic = 1
    if article.Title is None:
        title = ""
    else:
        title = article.Title

    if article.Abstract is None:
        abstract = ""
    else:
        abstract = article.Abstract

    text = title + " " + abstract
    text = text.replace("\n", "")
    try:
        result = extract_topic(text, "textrank")
        article.Topics = result
    except:
        exc_type, exc_value, exc_tb = sys.exc_info()
        print()
        # print(exc_tb.tb_frame)

        logger.ERROR(f"Error Line {exc_tb.tb_lineno}")
        logger.ERROR(f"Error {exc_value}")
        article.FlagExtractTopic = -1

    # Expire Module

    # topic_list = []
    # topic_list_phrase = []
    # if article.Abstract is not None:
    #     topic_list_phrase = extract_textrank(article.Abstract)

    # # print()
    # # print(f"Title : {article.Title}")

    # if topic_list_phrase is not None:

    #     for t in topic_list_phrase:
    #         if t.rank > 0.08:
    #             topic_list.append(t.text)

    #         # print(type(t))
    #         # print(t)
    #         # print(t.text)

    # # print(topic_list)
    # article.Topics = topic_list
    return article
