# Changelog
All notable changes to this project will be documented in this file.

## v0.0.5 2023-12-28

### Task
- RIS Parser
- pip install from source:
    - ModuleNotFoundError: No module named 'pydantic_settings'
    - ModuleNotFoundError: No module named 'langchain'
    - ModuleNotFoundError: No module named 'langchain_openai'
    - ModuleNotFoundError: No module named 'PyPDF2'
    - ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts. triplea 0.0.5 requires pydantic<2.0.0,>=1.10.4, but you have pydantic 2.6.1 which is incompatible.
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
