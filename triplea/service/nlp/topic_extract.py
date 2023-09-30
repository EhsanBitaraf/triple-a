# Expire Module

# import spacy
# import pytextrank
# from triplea.service.nlp.ner import get_title_ner

# nlp = spacy.load("en_core_web_sm")
# nlp.add_pipe("textrank")

# def extract_topicrank(text: str):
#     nlp = spacy.load("en_core_web_sm")
#     # add PyTextRank to the spaCy pipeline
#     # nlp.add_pipe("textrank")
#     nlp.add_pipe("topicrank")
#     doc = nlp(text)
#     # examine the top-ranked phrases in the document
#     # for phrase in doc._.phrases[:10]:
#     #     print(phrase.text)

#     return doc._.phrases[:10]


# def extract_positionrank(text: str):
#     nlp = spacy.load("en_core_web_sm")
#     # add PyTextRank to the spaCy pipeline
#     # nlp.add_pipe("textrank")
#     nlp.add_pipe("positionrank")
#     doc = nlp(text)
#     # examine the top-ranked phrases in the document
#     # for phrase in doc._.phrases[:10]:
#     #     print(phrase.text)

#     return doc._.phrases[:10]


# def extract_textrank(text: str):
#     # nlp = spacy.load("en_core_web_sm") # to up for performance
#     # add PyTextRank to the spaCy pipeline
#     # nlp.add_pipe("textrank")  # to up for performance
#     doc = nlp(text)
#     # examine the top-ranked phrases in the document
#     # for phrase in doc._.phrases[:10]:
#     #     print(phrase.text)

#     return doc._.phrases[:10]


# if __name__ == "__main__":
#     title = " Domestic violence and abuse (DVA) has a detrimental impact on the health and well-being of children and families but is commonly underreported, with an estimated prevalence of 5.5% in England and Wales in 2020. DVA is more common in groups considered vulnerable, including those involved in public law family court proceedings; however, there is a lack of evidence regarding risk factors for DVA among those involved in the family justice system. This study examines risk factors for DVA within a cohort of mothers involved in public law family court proceedings in Wales and a matched general population comparison group. We linked family justice data from the Children and Family Court Advisory and Support Service (Cafcass Cymru [Wales]) to demographic and electronic health records within the Secure Anonymised Information Linkage (SAIL) Databank. We constructed 2 study cohorts: mothers involved in public law family court proceedings (2011-2019) and a general population group of mothers not involved in public law family court proceedings, matched on key demographics (age and deprivation). We used published clinical codes to identify mothers with exposure to DVA documented in their primary care records and who therefore reported DVA to their general practitioner. Multiple logistic regression analyses were used to examine risk factors for primary care-recorded DVA. Mothers involved in public law family court proceedings were 8 times more likely to have had exposure to DVA documented in their primary care records than the general population group (adjusted odds ratio [AOR] 8.0, 95% CI 6.6-9.7). Within the cohort of mothers involved in public law family court proceedings, risk factors for DVA with the greatest effect sizes included living in sparsely populated areas (AOR 3.9, 95% CI 2.8-5.5), assault-related emergency department attendances (AOR 2.2, 95% CI 1.5-3.1), and mental health conditions (AOR 1.7, 95% CI 1.3-2.2). An 8-fold increased risk of DVA emphasizes increased vulnerabilities for individuals involved in public law family court proceedings. Previously reported DVA risk factors do not necessarily apply to this group of women. The additional risk factors identified in this study could be considered for inclusion in national guidelines. The evidence that living in sparsely populated areas and assault-related emergency department attendances are associated with increased risk of DVA could be used to inform policy and practice interventions targeting prevention as well as tailored support services for those with exposure to DVA. However, further work should also explore other sources of DVA, such as that recorded in secondary health care, family, and criminal justice records, to understand the true scale of the problem."
#     ner = get_title_ner(title)
#     for e in ner:
#         print(f"{e.label_} : {e.ents}")

#     print()
#     print('extract_topicrank : ')
#     l_topic = extract_topicrank(title)
#     for r in l_topic:
#         # print(f"topicrank : {r}")
#         print(f"{r.text}" )

#     print()
#     print('extract_positionrank : ')
#     l = extract_positionrank(title)
#     for r in l:
#         print(r.text)
#     print()
#     print('extract_textrank : ')
#     l = extract_textrank(title)
#     for r in l:
#         print(r.text)

#     # l_pmid = get_article_pmid_list_by_state(2)
#     # for id in l_pmid:
#     #     a = get_article_by_pmid(id)
#     #     try:
#     #         article = Article(**a.copy())
#     #     except:
#     #         print('error')

#     #     print()
#     #     print(article.Title)
#     #     ner = get_title_ner(article.Title)
#     #     for e in ner:
#     #         print(f'{e.label_} : {e.ents}')

#     #     print()
#     #     print('extract_topicrank : ')
#     #     l = extract_topicrank(article.Title)
#     #     for r in l:
#     #         print(r.text)
#     #     print()
#     #     print('extract_positionrank : ')
#     #     l = extract_positionrank(article.Title)
#     #     for r in l:
#     #         print(r.text)
#     #     print()
#     #     print('extract_textrank : ')
#     #     l = extract_textrank(article.Title)
#     #     for r in l:
#     #         print(r.text)

#     # text = "National eHealth Implementation"

#     # print()
#     # print(text)
#     # ner = get_title_ner(text)
#     # for e in ner:
#     #     print(f'{e.label_} : {e.ents}')

#     # print()
#     # print('extract_topicrank : ')
#     # l = extract_topicrank(text)
#     # for r in l:
#     #     print(r.text)
#     # print()
#     # print('extract_positionrank : ')
#     # l = extract_positionrank(text)
#     # for r in l:
#     #     print(r.text)
#     # print()
#     # print('extract_textrank : ')
#     # l = extract_textrank(text)
#     # for r in l:
#     #     print(r.text)

#     # l_pmid = get_article_pmid_list_by_state(2)
#     # for id in l_pmid:
#     #     a = get_article_by_pmid(id)
#     #     try:
#     #         article = Article(**a.copy())
#     #     except:
#     #         print('error')

#     #     print()
#     #     # print('extract_topicrank : ')
#     #     logger.INFO(article.Title)
#     #     l = extract_topicrank(article.Title)
#     #     for r in l:
#     #         print(f' topicrank {r.text}')
#     #         ner = get_title_ner(r.text)
#     #         for e in ner:
#     #             # print(f'{e.label_} : {e.ents}')
#     #             if e.label_ == 'MAJORTOPIC':
#     #                 logger.ERROR (e.ents)
#     #             if e.label_ == 'QUALIFIER':
#     #                 logger.WARNING (e.ents)
