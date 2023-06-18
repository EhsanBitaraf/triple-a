import sys
from triplea.schemas.article import Article
from triplea.service.click_logger import logger
from triplea.service.nlp.topic_extract import extract_textrank



def extract_topic_abstract(article: Article):
    article.FlagExtractTopic = 1
    topic_list = []
    topic_list_phrase = []
    if article.Abstract is not None:
        topic_list_phrase = extract_textrank(article.Abstract)

    # print()
    # print(f"Title : {article.Title}")
    
    if topic_list_phrase is not None:

        for t in topic_list_phrase:
            if t.rank > 0.08:
                topic_list.append(t.text)

            # print(type(t))
            # print(t)
            # print(t.text)
            
    # print(topic_list)
    article.Topics = topic_list
    return article
