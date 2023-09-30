# Expire Module

# from triplea.config.settings import ROOT
# import spacy


# nlp_ner = spacy.load(ROOT / "service" / "nlp" / "ner_model" / "model-best")


# def get_title_ner(title_text: str) -> tuple:
#     doc = nlp_ner(title_text)

#     # # For Display NER
#     # colors = {"MAJORTOPIC": "#F67DE3", "QUALIFIER": "#7DF6D9"}
#     # options = {"colors": colors}
#     # spacy.displacy.render(doc, style="ent", options= options, jupyter=False)

#     # # For print NER tag
#     # for e in doc.ents:
#     #     print(e.ents)
#     #     print(e.label_)

#     return doc.ents
