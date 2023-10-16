# Expire Module

# import spacy

# nlp = spacy.load("en_core_web_sm")


# # def triple_extract(text):
# #     # Parse the text with Spacy
# #     doc = nlp(text)

# #     # Extract subject-predicate-object (SPO) triples
# #     triples = []
# #     for chunk in doc.noun_chunks:
# #         if chunk.root.dep_ == "nsubj":
# #             subject = chunk.text
# #             predicate = chunk.root.head.text
# #             object = None
# #             for child in chunk.root.children:
# #                 if child.dep_ == "attr":
# #                     object = child.text
# #             if object:
# #                 triples.append((subject, predicate, object))


# #     return triples


# if __name__ == "__main__":
#     text = "Steve Jobs was the co-founder of Apple Inc."
#     # Parse the text with Spacy
#     doc = nlp(text)

#     # Extract subject-predicate-object (SPO) triples
#     triples = []
#     for chunk in doc.noun_chunks:
#         # print(chunk)
#         # print(chunk.root)
#         # print(chunk.root.dep_)
#         print(f"chunk.text : {chunk.text}")
#         print(f"predicate : {chunk.root.head.text} ({chunk.root.head.dep_})")
#         print(f"chunk.head : {chunk.head}")
#         for child in chunk.root.children:
#             pass
#             # print(f"    - {child.text} ({child.dep_})")

#         if chunk.root.dep_ == "nsubj":
#             subject = chunk.text
#             predicate = chunk.root.head.text
#             object = None
#             for child in chunk.root.children:
#                 if child.dep_ == "attr":
#                     object = child.text
#             if object:
#                 triples.append((subject, predicate, object))
