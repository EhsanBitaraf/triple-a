# Expire Module

# import spacy

# nlp = spacy.load("en_core_web_sm")

# def extract_triples(text):
#     triples = []
#     doc = nlp(text)

#     for sentence in doc.sents:
#         for token in sentence:
#             if "subj" in token.dep_:
#                 subject = token.text
#                 predicate = token.head.text
#                 object_ = token.head.head.text
#                 triples.append((subject, predicate, object_))

#     return triples

# if __name__ == "__main__":
#     text = "Steve Jobs was the co-founder of Apple Inc."
#     triples = extract_triples(text)
#     for triple in triples:
#         print(triple)
