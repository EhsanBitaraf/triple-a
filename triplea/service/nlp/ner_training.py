# Expire Module

# import json
# import spacy
# from spacy.tokens import DocBin
# from tqdm import tqdm
# from spacy.util import filter_spans
# from triplea.service.click_logger import logger


# def convert_label_studio_json_to_spacy_train_format(label_studio_file: str) -> dict:
#     with open(label_studio_file, "r") as f:
#         # 'project-4-at-2023-02-10-10-20-6a18f1dc.json'
#         data = json.load(f)

#     logger.INFO(f"Number of title article annotations in train data {len(data)}")

#     training_data = {"classes": ["MAJORTOPIC", "QUALIFIER"], "annotations": []}
#     for example in data:
#         temp_dict = {}
#         temp_dict["text"] = example["data"]["value"]
#         # print(temp_dict['text'])
#         temp_dict["entities"] = []
#         for annotation in example["annotations"]:
#             # print (json.dumps(annotation, indent=1))
#             for result in annotation["result"]:
#                 # print (json.dumps(result, indent=1))
#                 start = result["value"]["start"]
#                 end = result["value"]["end"]
#                 label = result["value"]["labels"][0].upper()
#                 temp_dict["entities"].append((start, end, label))
#         training_data["annotations"].append(temp_dict)

#     # print (json.dumps(training_data['annotations'][2], indent=1))
#     return training_data


# def generate_training_data(training_data: dict, training_data_file: str) -> None:
#     nlp = spacy.blank("en")  # load a new spacy model
#     doc_bin = DocBin()  # create a DocBin object

#     for training_example in tqdm(training_data["annotations"]):
#         text = training_example["text"]
#         labels = training_example["entities"]
#         doc = nlp.make_doc(text)
#         ents = []
#         for start, end, label in labels:
#             span = doc.char_span(start, end, label=label, alignment_mode="contract")
#             if span is None:
#                 print("Skipping entity")
#             else:
#                 ents.append(span)
#         filtered_ents = filter_spans(ents)
#         doc.ents = filtered_ents
#         doc_bin.add(doc)

#     # filename : "training_data.spacy"
#     doc_bin.to_disk(training_data_file)  # save the docbin object


# if __name__ == "__main__":
#     pass
#     # # Convert Label Studio Json format to Spacy Training data
#     # file = r"C:\Users\Bitaraf\Desktop\my-python-project\github\triple-a\triplea\service\ner_model\project-4-at-2023-02-10-10-20-6a18f1dc.json"
#     # data = convert_label_studio_json_to_spacy_train_format(file)

#     # # Save Spacy Training Data to docbin object file format
#     # training_data_file = r"C:\Users\Bitaraf\Desktop\my-python-project\github\triple-a\triplea\service\ner_model\training_data.spacy"
#     # generate_training_data(data,training_data_file)

#     # # Test Model
#     # ner = get_title_ner("Health complaints in individual visiting primary health care: population-based national electronic health records of Iran.")
#     # for e in ner:
#     #     print(f'{e.label_} : {e.ents}')
