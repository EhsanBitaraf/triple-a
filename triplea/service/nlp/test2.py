# Expire Module


# import spacy

# nlp = spacy.load("en_core_web_sm")
# text = "SpaCy is a powerful natural language processing library."
# text = "Steve Jobs was the co-founder of Apple Inc."
# text = "Credit and mortgage account holders must submit their requests"
# doc = nlp(text)
# for sentence in doc.sents:
#     print(sentence)
#     sentence.noun_chunks
#     for token in sentence:
#         if "subj" in token.dep_:
#             subject = token.text
#             predicate = token.head.text
#             object_ = token.head.head.text
#             print(f"token.text : {token.text}")
#             print(f"token.head.text : {token.head.text}")
#             # print(f"token.head.head.text : {token.head.head.text}")
#             for child in token.head.children:
#                     if child.text != token.text:
#                         print(f"    - children : {child.text} ({child.dep_})")
#                     if "obj" in child.dep_:
#                         object_ = child.text
#             # triples.append((subject, predicate, object_))
