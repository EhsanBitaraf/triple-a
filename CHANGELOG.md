# Changelog
All notable changes to this project will be documented in this file.

## v0.0.6 2024-02-13
### Task

- /triplea/service/llm/__init__.py", line 55
    raise Exception("chera")
- Export Mongo 2 Mongo
- Deduplication
- Change Affiliation
- Complete LLM-Fulltext pipeline
- Add CrossRef API : https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- Add import_ris_file into cli
- In Retracted publication. like this [artilce](https://pubmed.ncbi.nlm.nih.gov/36721396/)
```json
"PublicationTypeList": {
    "PublicationType": [
        {
            "#text": "Journal Article",
            "@UI": "D016428"
        },
        {
            "#text": "Retracted Publication",
            "@UI": "D016441"
        }
    ]
}
```
- Add [Altmetric API](/docs/client-api.md#altmetric-api)


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

### Task

- Expose `get_article_by_arxiv_id` to cli
- Article.Published must be fixed in pubmed and is string in Arxiv
- Data Extraction from Unstructured PDFs
    - https://www.analyticsvidhya.com/blog/2021/06/data-extraction-from-unstructured-pdfs/
    - https://unstructured-io.github.io/unstructured/core/partition.html
    - https://python.plainenglish.io/how-to-create-a-pdf2text-preprocessing-microservice-using-python-8b844b85c797
    - https://github.com/arXiv/arxiv-fulltext
- complete get_full_text
- move_state_forward may be error in TinyDB
- check all TinyDB

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
