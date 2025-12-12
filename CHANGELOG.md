# Changelog
All notable changes to this project will be documented in this file.


## v1.1.2 2025-12-12

### Improvements
- Initial version v1.1.2 and update poetry.lock with python 310


### Bug Fixes
- Fix poetry.lock for 20 security issue
- Fix get_tqdm()
- Fix triplea\service\llm\__init__.py with Backwards-compatible import for PromptTemplate
- Fix hkit in pyproject.toml


## v1.1.1 2025-07-20

### Task
- /triplea/service/llm/__init__.py", line 55
    raise Exception("chera")
- Export Mongo 2 Mongo
- Add import_ris_file into cli
- Expose `get_article_by_arxiv_id` to cli
- Article.Published must be fixed in pubmed and is string in Arxiv
- Data Extraction from Unstructured PDFs
    - https://www.analyticsvidhya.com/blog/2021/06/data-extraction-from-unstructured-pdfs/
    - https://unstructured-io.github.io/unstructured/core/partition.html
    - https://python.plainenglish.io/how-to-create-a-pdf2text-preprocessing-microservice-using-python-8b844b85c797
    - https://github.com/arXiv/arxiv-fulltext
- complete get_full_text


#### Task 2

TripleA Version

ModuleNotFoundError: No module named 'ratelimit'

- Fix _affiliation_mining_multiple_parser_in_list because this:
                            "city": [
                                "pittsburgh",
                                "pittsburgh",
                                "usa"
                            ]



----

---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
Cell In[2], line 6
      4 t_file = r"C:\Users\BT\Desktop\CodeBase\github\research-openehr\data-extraction-from-abstract-v3.json"
      5 id = "470"
----> 6 q = get_prompt_with_template_from_special_template_file(t_file, id)
      7 print(q)

File ~\Desktop\CodeBase\github\triple-a\triplea\service\llm\__init__.py:54, in get_prompt_with_template_from_special_template_file(template_file, dbuid)
     53 def get_prompt_with_template_from_special_template_file(template_file, dbuid: str):
---> 54     T = read_llm_template_from_file(template_file)
     55     prompt_template = PromptTemplate.from_template(T["template"])
     56     a = PERSIST.get_article_by_id(dbuid)

File ~\Desktop\CodeBase\github\triple-a\triplea\service\llm\config_template.py:147, in read_llm_template_from_file(llmtemplate_filename)
    144     # print(f"The file {llmtemplate} exists")
    145 else:
    146     print(f"The file {llmtemplate} does not exist")
--> 147     exit()
    148 with open(llmtemplate, encoding='utf-8') as f:
    149     d = json.load(f)

NameError: name 'exit' is not defined












### Improvements
- Check security
change last dependency in pyproject :

```
[tool.poetry.dependencies]
python = "^3.10"
click = "^8.1.7"
pydantic = "^2.6.1"
pydantic-settings = "^2.1.0"
tomli = "^2.0.1"
pymongo = "^4.6.1"
langchain-openai = "^0.0.5"
langchain = "^0.1.6"
tinydb = "^4.8.0"
networkx = "^3.2.1"
xmltodict = "^0.13.0"
nxviz = "^0.7.4"
netwulf = "^0.1.5"
ipykernel = "^6.29.2"
ipywidgets = "^8.1.2"
pypdf2 = "^3.0.1"
```

- Add `precalculate_llm_cost` and deprecated `precalculate`
- Add `from triplea.client.crossref import crossref_by_doi`
- Add `from triplea.client.altmetric import get_altmetric`
- Add `triplea.service.repository.pipeline_flag.go_get_enrich_data`
- Add `openalex_by_doi`
- Add `model_crossref_by_oid_without_pmid`
- Add `model_openalex_by_doi`
- Add `model_crossref_by_oid`
- Add `semanticscholar_by_doi`
- Add `model_semanticscholar_by_doi`
- Add `from triplea.client.crossref import crossref_by_doi`
- Add `from triplea.client.altmetric import get_altmetric` نباید خالی برگرداند هنگام خطا
- Add `triplea.service.repository.pipeline_flag.go_get_enrich_data`
- Add `EnrichedData` field to article object. 2025-10-20
- pip install -e "C:\Users\BT\Desktop\CodeBase\github\hkit" --Task
- Add clean_authors  in `triplea.service.repository.export.dataset`
- Add `normalize_issn` in `triplea.service.repository.export.dataset` version 1.1.1.003
- Add more field in affilation_integration in dataset(`_json_converter_03`) version 1.1.1.002
- Add `_get_affiliation_list_from_all_bank` and `_affiliation_mining_multiple_parser_in_list` and define AffiliationParseMethod.REGEX_API 2025-08-04
- Integrated all task improvment
- In version 0.0.7 the datamodel change. we change version to major

### Bug Fixes
- Improve & Fix logger in :
    - service\repository\state\initial.py
    - client\pubmed\__init__.py
    - service\repository\persist.py
    - service\repository\pipeline_core\__move_state_forward.py
    - service\repository\pipeline_core\__move_article_state_forward_by_id.py
    - service\repository\state\expand_details.py
    - service\repository\state\parsing_details_arxiv.py
    - service\repository\state\parsing_details_pubmed.py
    - service\repository\state\get_citation.py
    - service\repository\state\get_full_text.py
    - service\repository\import_file\ris_parser.py
    - move_state_until deprecated
- Fix _json_converter_03 for AffiliationIntegration
- Bug fix in `clean_publication_type` version 1.1.1.003
- Fix `from triplea.client.topic_extraction import extract_topic`
- Fix `from triplea.service.repository.state.custom.extract_topic import extract_topic_abstract`
- Fix `go_extract_topic`
- Fix `from triplea.service.repository.state.custom.affiliation_mining_multiple_parser`

## v0.0.7 2025-07-06

### Improvements
- Insert lib_llm.py to tripleA
- Add `_converter_authors_to_short` and `_json_converter_author_general` deprecated.
- Create `dataset.py` in triplea.service.repository.export for conver_df_to_csv, read_dataset_for_analysis, scimago_data_enrichment, clean_language_dataset, clean_publication_type, normalized_issn
- Create new version of dataset conversion `_json_converter_03`
- Create `get_tqdm` in `triplea.utils.general` for changing process bar
- Add EMBASE = 8 , ACM = 9 to `SourceBankType`
- Add `Language` and `Year` and `SerialNumber` and `links` and `PublicationType` to Article
- Add `CitationCount` field in Article

### Bug Fixes
- "A2" nicht Author ist Editor in `service\repository\import_file\ris_parser.py`
- Change and fix tqdm in `move_state_until`, `move_state_forward`, `go_extract_topic`
                        , `go_affiliation_mining`
                        , `export_engine`
- Fix `parsing_details_pubmed` for new article's fields
- Fix `_get_citation_pubmed`, `_get_citation_wos`, `_get_citation_scopus` and compatible with  `Article.CitationCount`

## v0.0.6 2024-02-13

### Improvements
- Add `DBUID` field in export. change in `export.engine`
- Add `SourceBankType.GOOGLESCHOLAR` 2025-01-22
- Add `convert_df2csv` to cookbook in `sample-export-engine-advanced`
- Update `update_cstate_by_id` in TinyDB
- Seperate `AAA_TOPIC_EXTRACT_ENDPOINT` and `AAA_AFFILIATION_PARSER_ENDPOINT` 2024-12-15
- Add IEEE , UNKNOWN to SourceBankType
- Update README.md
- Improve `json_converter_02`
- Add `delete_article_by_id`  2024-09-10
- Add `json_converter_02` for export and convert
- Add `change_CiteCrawlerDeep` in DAL
- Add `change_flag_affiliation_mining` in DAL
- Add `sample_import_ris_file.py` in Cookbook
- Add `change_status` 2024-07-01 
- Add `sample_calculate_llm_call` in Cookbook 2024-05-19
- Add `affiliation_mining_titipata_integration`
- Add new field for affiliation in `Version 0.0.6.005` 2024-04-08
- Change `pretty_print_dict` to `print_pretty_dict`
- Fix `import_ris_file` DEBUG process print
- Add Class Converter in `service.repository.export.unified_export_json.convert`
- Add `convert_unified2csv_dynamically`
- Add `update_llm_response`
- Add `export_engine`. This is very useful for export custom
- Add `_parse_ris_block` and `import_ris_file` [Issue #6](https://github.com/EhsanBitaraf/triple-a/issues/6)
- Add `insert_new_general_deduplicate_with_doi` , `is_article_exist_by_doi`
- Add `pretty_print_dict`

### Bug Fixes
- Fix authors in `json_converter_02` 2025-06-25
- Fix `model['DBUID'] = id`  in export engine
- Fix ris_parser in C3 for journal title in conference proccess in googlescholar
- Fix extra `\` in url of end points (AAA_AFFILIATION_PARSER_ENDPOINT) 2025-01-01
- Fix bug for loading llm template (encoding='utf-8')
- Add 'source' to `json_converter_02`
- Move `Database` and `Datasets` Directory from Repo 2024-12-15
- Fix `json_converter_02` for none AffiliationIntegration 2024-12-13
- Fix `export_engine` in `l_id = PERSIST.get_all_article_id_list()`
- Fix `question_with_template_for_llm`
- Fix Topic Extraction for method textrank, topicrank, positionrank in `Version 0.0.6.004`
- Fix bug in `get_article_list_from_pubmed_all_store_to_arepo`
- Fix FileNotFoundError for LLM Template 2024-03-24
- Fix AttributeError: 'Log' object has no attribute 'Error'. Did you mean: 'ERROR'? in line 13 cli/visualiza.py Version 0.0.6.003
- Fix `json_converter_01` for Scopus and Web of Sciense 
- Fix `go_affiliation_mining`
- Fix CLI pipline `FlagShortReviewByLLM`


## v0.0.5 2023-12-28

### Improvements
- Add `update_cstate_by_id` In SERVICE.REPOSITORY.PERSIST
- Add `precalculate` and `reset_flag_llm_by_function` in SERVICE.LLM
- Add `AAA_LLM_TEMPLATE_FILE` in SETTING
- Add FlagShortReviewByLLM
- Add `get_article_by_arxiv_id` Minor Version 003
- Add `convert_full_text2string` for converting fulltext pdf to string 
- Add `mongo_nav` for some query function for MongoDB
- Add `get_full_text`
- Add `article_embedding` and `scigenius_article_embedding` 2024-01-27
- Add unified_export_json
- Add `update_article_by_pmid` replace with `update_article_by_id`
- Add `get_article_id_list_by_cstate` replace with `get_article_pmid_list_by_cstate`
- Add `get_article_by_id` replace with `get_article_by_pmid`
- Add `get_all_article_id_list` replace  with`get_all_article_pmid_list`
- Add print_error in utils.general for unified Error printing
- Add Published, ArxivID, SourceBank field in Article

### Bug Fixes
- Repackaing pyproject.toml
- Fix parsing_details_pubmed.py", line 214 : `abstract_all = abstract_all + " " + abstract_part["#text"]`
- Fix `triplea/config/settings.py`, line 27 - FileNotFoundError: [Errno 2] No such file or directory: 'pyproject.toml'
- Fix `print_error()`
- Fix bug with pydantic new version 2024-02-03
- Fix session of extract_triple
- Fix tinydb.get_all_article_id_list

## v0.0.4 2023-10-14

### Improvements
- Add Package Application with Pyinstaller
- Add FlagAffiliationMining_TITIPATA from Api
- Add ParseMethod field in Affiliation

### Bug Fixes
- Fix go_affiliation_mining 2023-12-25
- Fix `E501` line too long
- Change path of `country.txt`
- Change 
        [tool.poetry.scripts]
        aaa = "triplea:cli.aaa"
  To
        [tool.poetry.scripts]
        aaa = "triplea.cli.aaa:main"
- Fix version in package  v0.0.4.002
- Fix GitHub Action `pyhton-flake`
- Package py2neo Lost. Disable `neo4j.py`


## v0.0.3 - 2023-09-27

### Improvements
- Add micro version
- Add `change_flag_extract_topic` in DAL
- All Github Action For Build Package
- Change go_extract_triple (Not Complete)
- Add cli.visualize_file  for visual graph file
- Add Client Topic Extraction
- Change Topics (list[str] to list[dict])

### Bug Fixes
- Fix Slow Request by session
- Fix Github Action
- Fix language parsing in `export_triplea_csvs_in_relational_mode_save_file`
- Remove spacy, transformers = {extras = ["torch"], version = "^4.30.0"}, pytextrank


## v0.0.2 - 2023-03-25

### Improvements
- Add `export_article` Alternative to export one article
- Add `export_triplea_csvs_in_relational_mode_save_file`
- Add `export_triplea_csv`
- Add Import File
- Add export triplea format
- 🥳Maryam Jafarpour's thesis defense took place 2023-09-20
- Add export rayyan format : `triplea\service\repository\export\rayyan_format.py`
- Add betweenness_centrality in jupyterlab
- Add sorted_closeness_centrality 2023-09-13 ([Issue #32](https://github.com/EhsanBitaraf/triple-a/issues/32))
- Add export_llm 2023-07-03
- Add selection-sampling
- Complete `go_affiliation_mining()` & `go_extract_topic()`
- Add Country Based Co-Authorship in Jupyter Lab
- Add CLI pipeline 2023-06-15
- Manage Triple in MongoDB but not in TinyDB
- Add `get_article_pmid_list_by_cstate()` :test_tube:Not Complete
- Add `extract_triples()` in NLP services 2023-06-13
- Complete CLI config ([Issue #2](https://github.com/EhsanBitaraf/triple-a/issues/2))
- Add `get_clustering_coefficient_per_node()` ([Issue #18](https://github.com/EhsanBitaraf/triple-a/issues/18)) :test_tube:`not complete`
- Add `get_avg_shortest_path_length_per_node()` ([Issue #17](https://github.com/EhsanBitaraf/triple-a/issues/17)) :test_tube:`not complete`
- Add "time report" and "elapsed time calculation report" to the `info` function ([Issue #16](https://github.com/EhsanBitaraf/triple-a/issues/16)) .
- Add graph_diameter
- Add Graph Radius ([Issue #11](https://github.com/EhsanBitaraf/triple-a/issues/11))
    , Number of Components([Issue #14](https://github.com/EhsanBitaraf/triple-a/issues/14)) to `Info()`
- Add Citation 2023-06-06
- Improve pyproject.toml
- Add remove_duplicate in cli.export

### Bug Fixes
- `$ black .\triplea\cli\`
- Fix Test
- Fix `sys.exit(1)` in CLI function
- Change `triplea\cli\export_graph.py` to `triplea\cli\export.py` 2023-09-19
- Fix DOI
- Fix Security [Issue #3](https://github.com/EhsanBitaraf/triple-a/security/dependabot/3)  Bump tornado from 6.2 to 6.3.2 [#24](https://github.com/EhsanBitaraf/triple-a/pull/24)
- Fix proccess_bar in export

## v0.0.1 - 2023-02-05

### Improvements
- Build Dockerfile
- Start flake8 activity 2023-03-05
- Optional Process Bars [Issue #6](https://github.com/EhsanBitaraf/triple-a/issues/6)
- progress bar for Emmanuel function [Issue #5](https://github.com/EhsanBitaraf/triple-a/issues/5)
- add arepo cli 2023-02-26
- Improve cli
- Add graph_extract_article_cited
- Add persist.get_all_article_pmid_list , general.move_state_until , cli.triplea , cli.import
- Add gdatarefresh
- Add export_to_neo4j
- Add Visualization InteractiveGraph
- Add convert_mongodb_to_tinydb
- Restructuring project
- Add Topic Extraction
- Improve environment variables
- Add convert_db
- Add DAL Mongodb
- Add Next CLI
- Add ner_title for NER article Title
- Add ganalysis in service for graph analysing by networkx
- Add Visualization
- Improve move_state_forward
- Add Export
- Improve Service
- Improve Model
- Add get_article_by_state
- Add DAL
- Add Project Structure
- Add settings

### Bug Fixes
- Fix get_all_article_pmid_list not implemented in MongoDB [Issue #3](https://github.com/EhsanBitaraf/triple-a/issues/3)
- Fix article.Title parsing
- Fix move_state_forward
