# Expire Module

# # https://github.com/bdmarius/python-knowledge-graph

# import json
# import spacy
# from spacy.lang.en import English

# nlp_model = spacy.load('en_core_web_sm')
# nlp_model.add_pipe("merge_noun_chunks")
# logType = 0
# def pLog(logText):
#     if logType == 1:
#         print(logText)


# def getSentences(text: str) -> str:
#     """Get Sentences from praghraph.

#     Args:
#         text (str): the paragraph to be chunck.

#     Returns:
#         A text variable of <class 'str'> after separating Sentence.

#     Examples:
#         >>> getSentences("*hello to people**")
#         'hello to people'
#     """
#     nlp = English()
#     #nlp.add_pipe(nlp.create_pipe('sentencizer'))
#     nlp.add_pipe('sentencizer')

#     document = nlp(text)
#     return [sent.text.strip() for sent in document.sents]

# def printToken(token):
#     if "obj" in token.dep_:
#     #if token.dep_ in ("obj" , "subj"):
#         pLog(token.text + "----------------------------->" + token.dep_)
#     elif  "subj" in token.dep_:
#         pLog(token.text + "-->----->-------->------->----->" + token.dep_)
#     else:
#         pLog(token.text + "->" + token.dep_)

# def appendChunk(original, chunk):
#     return original.strip() + ' ' + chunk.strip()

# def isRelationCandidate(token):
#     #deps = ["ROOT", "adj", "attr", "agent", "amod"]
#     deps = ["ROOT"]
#     return any(subs in token.dep_ for subs in deps)

# def isConstructionCandidate(token):
#     deps = ["compound", "prep", "conj", "mod"]
#     return any(subs in token.dep_ for subs in deps)

# def processSubjectObjectPairs(tokens):
#     # version 3 chunk
#     # Merge noun chunks into a single token. Also available via the string name "merge_noun_chunks".
#     # nlp_model.add_pipe("merge_noun_chunks")
#     # in main
#     subject = ''
#     object = ''
#     relation = ''
#     subjectConstruction = ''
#     objectConstruction = ''
#     firstObject = False
#     firstRelation = False
#     firstSubject = False
#     i = 0
#     ROOTposition = tokens.__len__()
#     for token in tokens:
#         printToken(token)
#         if "punct" in token.dep_:
#             continue
#         if isRelationCandidate(token):
#             pLog("relation ------------> " +  token.lemma_)
#             if firstRelation == False:
#                 relation = appendChunk(relation, token.lemma_)
#                 ROOTposition = token.i
#                 if "prep" in tokens[token.i + 1].dep_: # like focus on
#                     relation = appendChunk(relation, tokens[token.i + 1].lemma_)
#                 if "agent" in tokens[token.i + 1].dep_: # like guided by
#                     relation = appendChunk(relation, tokens[token.i + 1].lemma_)
#                 if "attr" in tokens[token.i + 1].dep_ and  tokens[token.i + 1].pos_ == "NOUN" : # like Cytoreductive surgery is the mainstay[attr]
#                     object = tokens[token.i + 1].text
#                     firstObject = True
#                 if tokens[token.i + 1].dep_ == "aux":
#                     relation = appendChunk(relation, tokens[token.i + 1].lemma_)
#                     relation = appendChunk(relation, tokens[token.i + 2].lemma_)

#                 firstRelation = True
#         if isConstructionCandidate(token):
#             pLog("isConstructionCandidate")
# #             if subjectConstruction:
# #                 pLog("subjectConstruction ------------> " + subjectConstruction)
# #                 subjectConstruction = appendChunk(subjectConstruction, token.text)
# #                 pLog("subjectConstruction ------------> " + subjectConstruction)
# #             if objectConstruction:
# #                 pLog("objectConstruction ------------> " + objectConstruction)
# #                 objectConstruction = appendChunk(objectConstruction, token.text)
# #                 pLog("objectConstruction ------------> " + objectConstruction)
#         if "subj" in token.dep_:
#             if firstSubject == False:
#                 pLog("subject num ------------> " + str(i))
#                 pLog("subject ----------------> " + subject)
#                 subject = appendChunk(subject, token.text)
#                 pLog("subject ----------------> " + subject)
#                 subject = appendChunk(subjectConstruction, subject)
#                 pLog("subject ----------------> " + subject)
#                 subjectConstruction = ''
#                 pLog(str(i))
#                 if i != 0 :
#                     if "amod" in tokens[i-1].dep_:
#                         pLog("Inja")
#                         subject = tokens[i-1].text + subject
#                     if "compound" in tokens[i-1].dep_:
#                         subject = tokens[i-1].text + subject
#                     pLog("subject tokens[i-1].text (" + tokens[i-1].text + ") ----------------> " + subject)
#                 firstSubject = True

#         if "obj" in token.dep_:
#             if firstObject == False:
#                 if token.i > ROOTposition :
#                     object = appendChunk(object, token.text)
#                     object = appendChunk(objectConstruction, object)
#                     objectConstruction = ''
#                     if i != 0 :
#                         if "conj" in tokens[i-1].dep_:
#                             object = tokens[i-1].text + object
#                     firstObject = True
#         i = i + 1
#         # # I doubt it can be a list or it is one
#         # print(subject.strip() + "," + relation.strip() + "," + object.strip())

#     pLog (subject.strip() + "," + relation.strip() + "," + object.strip())
#     return (subject.strip(), relation.strip(), object.strip())

# def processSentence(sentence):
#     tokens = nlp_model(sentence)
#     return processSubjectObjectPairs(tokens)

# def extractRelaction(text):
#     sentences = getSentences(text)
#     triples = []
#     for sentence in sentences:
#         triples.append(processSentence(sentence))
#     return triples


# def extract_triples(text:str):
#     sentences = getSentences(text)

#     triples = []
#     kg = []
#     for sentence in sentences:
#         dict = {}

#         rel = processSentence(sentence)
#         dict['source'] = rel[0]
#         dict['edge'] = rel[1]
#         dict['target'] = rel[2]
#         dict['sentence'] = sentence
#         kg.append(dict)


#     return kg

# if __name__ == "__main__":
#     text = "SpaCy is a powerful natural language processing library."
#     extract_triples(text)
