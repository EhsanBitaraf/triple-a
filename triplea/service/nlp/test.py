# Expire Module

# import spacy

# # Load the English model
# nlp = spacy.load('en_core_web_sm')

# # Define the text to extract information from
# text = "John Smith is the CEO of Acme Inc. The company is based in New York City."

# # Parse the text with Spacy
# doc = nlp(text)

# # Extract named entities and their labels
# entities = [(ent.text, ent.label_) for ent in doc.ents]
# print("Named entities:", entities)

# # Extract subject-verb-object triples
# triples = []
# for sent in doc.sents:
#     subtree = []
#     for tok in sent:
#         if tok.dep_ in ('xcomp', 'ccomp'):
#             subtree.append(tok)
#     if len(subtree) == 1 and subtree[0].pos_ == 'VERB':
#         subject = [tok for tok in subtree[0].lefts if tok.dep_ == 'nsubj']
#         object = [tok for tok in subtree[0].rights if tok.dep_ == 'dobj' or tok.dep_ == 'attr']
#         if subject and object:
#             triples.append((subject[0], subtree[0], object[0]))
# for triple in triples:
#     print("Triple:", (triple[0].text, triple[1].text, triple[2].text))
