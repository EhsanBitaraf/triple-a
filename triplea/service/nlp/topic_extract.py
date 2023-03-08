import spacy
import pytextrank
from triplea.service.nlp.ner import get_title_ner


def extract_topicrank(text: str):
    nlp = spacy.load("en_core_web_sm")
    # add PyTextRank to the spaCy pipeline
    # nlp.add_pipe("textrank")
    nlp.add_pipe("topicrank")
    doc = nlp(text)
    # examine the top-ranked phrases in the document
    # for phrase in doc._.phrases[:10]:
    #     print(phrase.text)

    return doc._.phrases[:10]


def extract_positionrank(text: str):
    nlp = spacy.load("en_core_web_sm")
    # add PyTextRank to the spaCy pipeline
    # nlp.add_pipe("textrank")
    nlp.add_pipe("positionrank")
    doc = nlp(text)
    # examine the top-ranked phrases in the document
    # for phrase in doc._.phrases[:10]:
    #     print(phrase.text)

    return doc._.phrases[:10]


def extract_textrank(text: str):
    nlp = spacy.load("en_core_web_sm")
    # add PyTextRank to the spaCy pipeline
    # nlp.add_pipe("textrank")
    nlp.add_pipe("textrank")
    doc = nlp(text)
    # examine the top-ranked phrases in the document
    # for phrase in doc._.phrases[:10]:
    #     print(phrase.text)

    return doc._.phrases[:10]


if __name__ == "__main__":
    title = "Health complaints in individual visiting primary health care: population-based national electronic health records of Iran."
    ner = get_title_ner(title)
    for e in ner:
        print(f"{e.label_} : {e.ents}")

    l_topic = extract_topicrank(title)
    for r in l_topic:
        print(r)
        print(r.text)

    # l_pmid = get_article_pmid_list_by_state(2)
    # for id in l_pmid:
    #     a = get_article_by_pmid(id)
    #     try:
    #         article = Article(**a.copy())
    #     except:
    #         print('error')

    #     print()
    #     print(article.Title)
    #     ner = get_title_ner(article.Title)
    #     for e in ner:
    #         print(f'{e.label_} : {e.ents}')

    #     print()
    #     print('extract_topicrank : ')
    #     l = extract_topicrank(article.Title)
    #     for r in l:
    #         print(r.text)
    #     print()
    #     print('extract_positionrank : ')
    #     l = extract_positionrank(article.Title)
    #     for r in l:
    #         print(r.text)
    #     print()
    #     print('extract_textrank : ')
    #     l = extract_textrank(article.Title)
    #     for r in l:
    #         print(r.text)

    # text = "National eHealth Implementation"

    # print()
    # print(text)
    # ner = get_title_ner(text)
    # for e in ner:
    #     print(f'{e.label_} : {e.ents}')

    # print()
    # print('extract_topicrank : ')
    # l = extract_topicrank(text)
    # for r in l:
    #     print(r.text)
    # print()
    # print('extract_positionrank : ')
    # l = extract_positionrank(text)
    # for r in l:
    #     print(r.text)
    # print()
    # print('extract_textrank : ')
    # l = extract_textrank(text)
    # for r in l:
    #     print(r.text)

    # l_pmid = get_article_pmid_list_by_state(2)
    # for id in l_pmid:
    #     a = get_article_by_pmid(id)
    #     try:
    #         article = Article(**a.copy())
    #     except:
    #         print('error')

    #     print()
    #     # print('extract_topicrank : ')
    #     logger.INFO(article.Title)
    #     l = extract_topicrank(article.Title)
    #     for r in l:
    #         print(f' topicrank {r.text}')
    #         ner = get_title_ner(r.text)
    #         for e in ner:
    #             # print(f'{e.label_} : {e.ents}')
    #             if e.label_ == 'MAJORTOPIC':
    #                 logger.ERROR (e.ents)
    #             if e.label_ == 'QUALIFIER':
    #                 logger.WARNING (e.ents)
