# # Expire Module

# from triplea.schemas.article import Article, NamedEntity
# from triplea.service.nlp.ner import get_title_ner


# def ner_title(article: Article) -> Article:
#     article.State = 4
#     ner = get_title_ner(article.Title)
#     l_ner = []
#     for e in ner:
#         my_ner = NamedEntity()
#         if len(e.ents) > 1:
#             raise NotImplementedError
#         my_ner.Label = e.label_
#         # print(type(e.ents[0]))
#         my_ner.Entity = e.ents[0].text
#         l_ner.append(my_ner)
#         # print(f'{e.label_} : {e.ents}')

#     if len(l_ner) > 0:
#         article.NamedEntities = l_ner

#     return article
