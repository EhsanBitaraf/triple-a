# Triple-a - *Article Analysis Assistant*

Triple-A is a tool that can be used to create a repository of scientific articles and perform a series of citation graph analysis, bibilometric analysis, and automatic data extraction processes on this repository.

This program somehow creates a network of article references and provides a connection between authors and keywords, these things are usually called "[**Citation Graph**](https://en.wikipedia.org/wiki/Citation_graph)".

There are various software and online systems for this, a brief review of which can be found [here](docs/related-work.md).

This tool gives you the power to create a graph of articles and analyze it. This tool is designed as a **CLI** (command-line interface) and you can use it as a Python library.

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

[![commits](https://badgen.net/github/commits/EhsanBitaraf/triple-a/main)](https://github.com/EhsanBitaraf/triple-a/commits/main?icon=github&color=green)
[![GitHub Last commit](https://img.shields.io/github/last-commit/EhsanBitaraf/triple-a)](https://github.com/EhsanBitaraf/triple-a/main)
![Open Issue](https://img.shields.io/github/issues-raw/EhsanBitaraf/triple-a)

![Repo Size](https://img.shields.io/github/repo-size/EhsanBitaraf/triple-a)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/EhsanBitaraf/triple-a)
![Downloads](https://img.shields.io/github/downloads/EhsanBitaraf/triple-a/total)

[![GitHub tag](https://img.shields.io/github/tag/EhsanBitaraf/triple-a.svg)](https://GitHub.com/EhsanBitaraf/triple-a/tags/)
![Release](https://img.shields.io/github/release/EhsanBitaraf/triple-a)
![Release](https://img.shields.io/github/release-date/EhsanBitaraf/triple-a)

<!-- ![PyPI - Wheel](https://img.shields.io/pypi/EhsanBitaraf/triple-a) -->

[![PyPI version](https://badge.fury.io/py/triplea.svg)](https://badge.fury.io/py/triplea)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/triplea)

![Build and push images](https://github.com/EhsanBitaraf/triple-a/workflows/push%20docker%20image/badge.svg)

![Testing](https://github.com/EhsanBitaraf/triple-a/actions/workflows/test-poetry-action.yml/badge.svg)

![Code Quality](https://github.com/EhsanBitaraf/triple-a/actions/workflows/python-flake.yml/badge.svg)





<!-- test this :

https://badge.fury.io/for/py/Triple-a -->

<!-- [![GitHub commits](https://img.shields.io/github/commits-since/EhsanBitaraf/triple-a/v1.0.0.svg)](https://github.com/EhsanBitaraf/triple-a/commit/master) -->


# Table of contents

- [Main Features](#-main-features)
- [How to Install](#how-to-install)
  - [Installation From Source Code](#installation-from-source-code)
  - [Installation from package](#installation-from-package)
- [How to Work with the Program](#how-to-work-with-the-program)
  - [Functional Use](#functional-use)
  - [Command Line (CLI) Use](#command-line-cli-use)
- [Testing](#testing)
  - [Running All Tests](#running-all-tests)
  - [Running Tests in a Specific Directory](#running-tests-in-a-specific-directory)
  - [Running Tests with Coverage](#running-tests-with-coverage)
  - [Additional Coverage Reports](#additional-coverage-reports)
- [Dependencies](#dependencies)
  - [Graph Analysis](#graph-analysis)
  - [Natural Language Processing (NLP)](#natural-language-processing-nlp)
  - [Data Storage](#data-storage)
  - [Visualization of Networks](#visualization-of-networks)
  - [Command-Line Interface (CLI)](#command-line-interface-cli)
  - [Packaging and Dependency Management](#packaging-and-dependency-management)
- [Use Case](#use-case)
  - [Breast Cancer Dataset](#breast-cancer-dataset)
  - [Bio-Bank Dataset](#bio-bank-dataset)
  - [Registry of Breast Cancer Dataset](#registry-of-breast-cancer-dataset)
- [Public Dataset](#public-dataset)
  - [Topic Extraction Dataset - Related to Breast Cancer Therapy](#topic-extraction-dataset---related-to-breast-cancer-therapy)
  - [Coronary Artery Disease Clinical Trial Articles](#coronary-artery-disease-clinical-trial-articles)
  - [MIE Articles Dataset](#mie-articles-dataset)
- [Graph Visualization](#graph-visualization)
- [Graph Analysis](#graph-analysis)
- [Knowledge Extraction](#knowledge-extraction)
- [Related Article](#related-article)
- [Code Quality](#code-quality)
- [Citation](#citation)
- [License](#license)



# 🎮 Main Features
- **Repository Creation**: Collect and store articles based on a search strategy.
- **Citation Graph Analysis**: Generate and analyze citation networks between articles.
- **Bibliometric Analysis**: Perform advanced [bibliometric analysis](https://researchguides.uic.edu/bibliometrics).
- **Retrieval-Augmented Generation (RAG)**: Automatically retrieve and analyze content for a domain of articles.
- **Single Article Analysis**: Analyze individual articles.
- **Network Analysis**: Conduct detailed network analysis at both node and overall graph levels.
- **Bibliography Import**: Easily import bibliography files in various formats (e.g., `.bib`, `.ris`).
- **Topic Extraction**: Perform topic extraction using an external service.
- **Affiliation Parsing**: Perform affiliation parsing using an external service.


# How to Install 

## Installation From Source Code

### Step 1: Clone the Repository
First, clone the TripleA repository from GitHub using one of the following commands:

For HTTPS:
```shell
git clone https://github.com/EhsanBitaraf/triple-a.git
```

For SSH:
```shell
git clone git@github.com:EhsanBitaraf/triple-a.git
```

### Step 2: Create a Python Virtual Environment
Navigate to the repository directory and create a Python virtual environment to isolate your project dependencies:

```shell
python -m venv venv
```

### Step 3: Activate the Virtual Environment

For **Windows**:
```shell
$ .\venv\Scripts\activate
```

For **Linux/macOS**:
```shell
$ source venv/bin/activate
```

### Step 4: Install Poetry
[Poetry](https://python-poetry.org/) is used for managing dependencies in this project. If you don't already have Poetry installed, install it using pip:

```shell
pip install poetry
```

### Step 5: Install Dependencies
Once Poetry is installed, use it to install all the required dependencies for the project:

```shell
poetry install
```

### Step 6: Run the CLI
After the dependencies are installed, you can run the CLI by executing the following command:

```shell
poetry run python triplea/cli/aaa.py
```

This will launch the TripleA CLI, where you can interact with the various commands available.

### Step 7: (Optional) Configure Environment Variables
To customize your environment, you can create a `.env` file in the root directory of the project. Refer to the [installation from package instructions](#step-4-configure-environment-variables) for the full list of environment variables you can set.

If the `.env` file is not created, default values will be used as specified in the package.



## Installation from package
It is recommended to create a Python virtual environment before installing the package to keep your project dependencies isolated. You can do so by running the following commands:

### Step 1: Create a Python Virtual Environment
```sh
$ python -m venv venv
```

### Step 2: Activate the Virtual Environment
For Windows:
```sh
$ .\venv\Scripts\activate
```

For macOS/Linux:
```sh
$ source venv/bin/activate
```

### Step 3: Install the Package
You can install the [TripleA package](https://pypi.org/project/triplea/) from PyPI using pip:

```sh
$ pip install triplea
```

Alternatively, you can install the package directly from the GitHub repository:

```sh
$ pip install git+https://github.com/EhsanBitaraf/triple-a
```

### Step 4: Configure Environment Variables
Create a `.env` file in the root of your project to set environment variables for the package. This file should contain the following key-value pairs:

```
TRIPLEA_DB_TYPE = TinyDB
AAA_TINYDB_FILENAME = articledata.json
AAA_MONGODB_CONNECTION_URL = mongodb://localhost:27017/
AAA_MONGODB_DB_NAME = articledata
AAA_TPS_LIMIT = 1
AAA_PROXY_HTTP = 
AAA_PROXY_HTTPS = 
AAA_REFF_CRAWLER_DEEP = 1
AAA_CITED_CRAWLER_DEEP = 1
AAA_TOPIC_EXTRACT_ENDPOINT = http://localhost:8001/api/v1/topic/
AAA_CLIENT_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0"
```

If the `.env` file is not created, the default values will be used:
```
TRIPLEA_DB_TYPE = TinyDB
AAA_TINYDB_FILENAME = default-tiny-db.json
AAA_TPS_LIMIT = 1
AAA_REFF_CRAWLER_DEEP = 1
AAA_CITED_CRAWLER_DEEP = 1
AAA_TOPIC_EXTRACT_ENDPOINT = http://localhost:8001/api/v1/topic/
AAA_CLIENT_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0"
```

For reference, the latest version of a sample `.env` file can be found [here](https://github.com/EhsanBitaraf/triple-a/blob/main/triplea/config/environment_variable/.env.sample).

### Step 5: Running the CLI
You can access the TripleA CLI by running the following command:

```sh
$ aaa --help
```

The output will be:
```sh
Usage: aaa [OPTIONS] COMMAND [ARGS]...

Options:
  -v, --version
  --help         Show this message and exit.

Commands:
  analysis        Analysis Graph.
  config          Configuration additional setting.
  export          Export article repository in specific format.
  export_article  Export Article by identifier.
  export_graph    Export Graph.
  export_llm      Export preTrain LLM.
  go              Moves the articles state in the Arepo until end state.
  import          Import article from specific file format to article...
  importbib       Import article from .bib, .enw, .ris file format.
  ner             Single NER with custom model.
  next            Moves the articles state in the Arepo from the current...
  pipeline        Run Custom Pipeline in arepo.
  search          Search query from PubMed and store to Arepo.
```

*Note:*

- The visualization feature is only available in the source version of the package.

*Tutorial:*

For additional guides and programming examples beyond using the package, please refer to the [cookbook section](https://github.com/EhsanBitaraf/triple-a/blob/main/cookbook/README.md).



# How to Work with the Program
Once the program is installed, you can utilize it both as a CLI tool and by calling its functions directly within your Python code. Below is a step-by-step guide for retrieving articles, processing them through various stages, and performing additional tasks like topic extraction and affiliation mining.

## Functional Use

### Step 1 - Get Articles from Arxiv
You can retrieve articles from Arxiv using a specific search query and store them into the article repository (Arepo). Here's an example using a search string for large language models:

```python
arxiv_search_string = '(ti:“Large language model” OR ti:“Large language models” OR (ti:large AND ti:“language model”) OR (ti:large AND ti:“language models”) OR (ti:“large language” AND ti:model) OR (ti:“large language” AND ti:models) OR ti:“language model” OR ti:“language models” OR ti:LLM OR ti:LLMs OR ti:“GPT models” OR ti:“GPT model” OR ti:Gpt OR ti:gpts OR ti:Chatgpt OR ti:“generative pre-trained transformer” OR ti:“bidirectional encoder representations from transformers” OR ti:BERT OR ti:“transformer-based model” OR (ti:transformer AND ti:model) OR (ti:transformers AND ti:model) OR (ti:transformer AND ti:models) OR (ti:transformers AND ti:models)) AND (ti:Evaluation OR ti:Evaluat* OR ti:Assessment OR ti:Assess* OR ti:Validation OR ti:Validat* OR ti:Benchmarking OR ti:Benchmark*)'
get_article_list_from_arxiv_all_store_to_arepo(arxiv_search_string, 0, 5000)
```

This fetches articles based on the query and stores up to 5000 articles into the repository.

### Step 2 - Get Articles from PubMed
Similarly, you can retrieve articles from PubMed using a custom search string and store them in the repository:

```python
pubmed_search_string = '("Large language model"[ti] OR "Large language models"[ti] OR (large[ti] AND "language model"[ti]) OR (large[ti] AND "language models"[ti]) OR ("large language"[ti] AND model[ti]) OR ("large language"[ti] AND models[ti]) OR "language model"[ti] OR "language models"[ti] OR LLM[ti] OR LLMs[ti] OR "GPT models"[ti] OR "GPT model"[ti] OR Gpt[ti] OR gpts[ti] OR Chatgpt[ti] OR "generative pre-trained transformer"[ti] OR "bidirectional encoder representations from transformers"[ti] OR BERT[ti] OR "transformer-based model"[ti] OR (transformer[ti] AND model[ti]) OR (transformers[ti] AND model[ti]) OR (transformer[ti] AND models[ti]) OR (transformers[ti] AND models[ti])) AND (Evaluation[ti] OR Evaluat*[ti] OR Assessment[ti] OR Assess*[ti] OR Validation[ti] OR Validat*[ti] OR Benchmarking[ti] OR Benchmark*[ti])'
get_article_list_from_pubmed_all_store_to_arepo(pubmed_search_string)
```

This stores all relevant articles from PubMed into the repository based on the specified query.

### Step 3 - Get Information from Repository
To print article information that has been stored in the repository, you can use the following command:

```python
PERSIST.print_article_info_from_repo()
```

This will print out details about the articles that have been saved so far.

### Step 4 - Move Articles from State 0 to State 1 (Save Article Details)
The articles are initially stored in state 0. Use this command to move them to state 1, where their original details (in JSON format) will be saved:

```python
move_state_forward(0)
```

### Step 5 - Move Articles from State 1 to State 2 (Parse Article Information)
To parse the article's detailed information and move it from state 1 to state 2:

```python
move_state_forward(1)
```

### Step 6 - Move Articles from State 2 to State 3 (Get Citations)
This step retrieves citation data for the articles and moves them to state 3:

```python
move_state_forward(2)
```

### Step 7 - Move Articles from State 3 to State 4 (Get Full Text)
Fetch the full text of the articles and move them from state 3 to state 4:

```python
move_state_forward(3)
```

### Step 8 - Move Articles from State 4 to State 5 (Convert Full Text to String)
In this step, the full text of the articles is converted to a string format for further analysis:

```python
move_state_forward(4)
```

### Custom Pipeline Operations

Once the articles have been processed through the various states, you can perform more advanced operations in the custom pipeline.

#### 1. Extract Topics from Articles
This function will run the topic extraction process on the articles:

```python
cPIPELINE.go_extract_topic()
```

#### 2. Perform Affiliation Mining
You can extract affiliation information from articles using the method specified ("Titipata" in this case):

```python
cPIPELINE.go_affiliation_mining(method="Titipata")
```

#### 3. Extract Triples (Subject-Predicate-Object Relations)
To extract triples (semantic relations) from the articles:

```python
cPIPELINE.go_extract_triple()
```

#### 4. Generate Short Review Article with LLM
This function allows you to create a brief review of the articles using a large language model (LLM):

```python
cPIPELINE.go_article_review_by_llm()
```

#### 5. Export Data
Finally, to export the processed data (e.g., triples) in a CSV format:

```python
export_triplea_csvs_in_relational_mode_save_file("export.csv")
```

This saves the exported data into a CSV file named `export.csv`.


#### Some practices

get list of PMID in state 0
```python
term = '("Electronic Health Records"[Mesh]) AND ("National"[Title/Abstract]) AND Iran'
get_article_list_all_store_to_kg_rep(term)
```

move from state 1
```python
move_state_forward(1)
```

get list of PMID in state 0 and save to file for debugginf use
```python
    data = get_article_list_from_pubmed(1, 10,'("Electronic Health Records"[Mesh]) AND ("National"[Title/Abstract])')
    data = get_article_list_from_pubmed(1, 10,'"Electronic Health Records"')
    data1= json.dumps(data, indent=4)
    with open("sample1.json", "w") as outfile:
        outfile.write(data1)
```

open before file for debugging use
```python
    f = open('sample1.json')
    data = json.load(f)
    f.close()
```

get one article from kg and save to file
```python
    data = get_article_by_pmid('32434767')
    data= json.dumps(data, indent=4)
    with open("one-article.json", "w") as outfile:
        outfile.write(data)
```

Save Title for Annotation
```python
    file =  open("article-title.txt", "w", encoding="utf-8")
    la = get_article_by_state(2)
    for a in la:
        try:
            article = Article(**a.copy())
        except:
            pass
        file.write(article.Title  + "\n")
```

##### Training NER for Article Title

You can use NLP(Natural Language Processing) methods to extract information from the structure of the article and add it to your graph. For example, you can extract NER(Named-entity recognition) words from the title of the article and add to the graph. [Here's how to create a custom NER](docs/training-ner.md).



## Command Line (CLI) Use

By using the following command, you can see the command completion `help`. Each command has a separate `help`.

```shell
python .\triplea\cli\aaa.py  --help
```

output:

![](https://github.com/EhsanBitaraf/triple-a/tree/main/docs/assets/img/aaa-help.png)


### Get and Save list of article identifier base on search term

Get list of article identifier like PMID base on search term and save into knowledge repository in first state (0):

use this command:
```shell
python .\triplea\cli\aaa.py search --searchterm [searchterm]
```

Even the PMID itself can be used in the search term.
```shell
python .\triplea\cli\aaa.py search --searchterm 36467335
```

output:

![](https://github.com/EhsanBitaraf/triple-a/tree/main/docs/assets/img/aaa-search.png)

### Move core pipeline state
The preparation of the article for extracting the graph has different steps that are placed in a pipeline. Each step is identified by a number in the state value. The following table describes the state number:

*List of state number*

|State|Short Description|Description|
|-----|-----------------|-----------|
|0    |article identifier saved|At this stage, the article object stored in the data bank has only one identifier, such as the PMID or DOI identifier|
|1    |article details article info saved (json Form)|Metadata related to the article is stored in the `OriginalArticle` field from the `SourceBank`, but it has not been parsed yet|
|2    |parse details info|The contents of the `OriginalArticle` field are parsed and placed in the fields of the Article object.|
|3    |Get Citation      ||
|4    |Get Full Text     |At this stage, the articles that are open access and it is possible to get their full text are taken and added to the bank|
|5    |Convert full text to string     ||
|-1   |Error             |if error happend in move state 1 to 2|
|-2   |Error             |if error happend in move state 2 to 3|

There are two ways to run a pipeline. In the first method, we give the number of the existing state and all the articles in this state move forward one state.
In another method, we give the final state number and each article under that state starts to move until it reaches the final state number that we specified.
The first can be executed with the `next` command and the second with the `go` command.

With this command move from current state to the next state
```shell
python .\triplea\cli\aaa.py next --state [current state]
```

for example move all article in state 0 to 1:
```shell
python .\triplea\cli\aaa.py next --state 0
```
output:

![](https://github.com/EhsanBitaraf/triple-a/tree/main/docs/assets/img/aaa-next.png)


`go` command:
```shell
python .\triplea\cli\aaa.py go --end [last state]
```

```shell
python .\triplea\cli\aaa.py go --end 3
```

output:

![](https://github.com/EhsanBitaraf/triple-a/tree/main/docs/assets/img/aaa-go.png)


### Run custom pipeline
Apart from the core pipelines that should be used to prepare articles, customized pipelines can also be used. Custom pipelines may be implemented to extract knowledge from texts and NLP processing. These pipelines themselves can form a new graph other than the citation graph or in combination with it.


List of Custom Pipeline

|Action|Tag Name|Description|Prerequisite|
|------|--------|-----------|------------|
|Triple extraction from article abstract      |FlagExtractKG        ||At least core state 2|
|Topic extraction from article abstract       |FlagExtractTopic     ||At least core state 2|
|Convert Affiliation text to structural data  |FlagAffiliationMining|This is simple way for parse Affiliation text |At least core state 2|
|Convert Affiliation text to structural data  |FlagAffiliationMining_Titipata|use [Titipat Achakulvisut Repo](https://github.com/titipata/affiliation_parser) for parsing Affiliation text|At least core state 2|
|Text embedding abstract and send to SciGenius|FlagEmbedding        ||At least core state 2|
|Title and Abstract Review by LLM             |FlagShortReviewByLLM ||At least core state 2|

#### NER Article Title
You can try the NER method to extract the major topic of the article's title by using the following command. This command is independent and is used for testing and is not stored in the Arepo.

```shell
python .\triplea\cli\ner.py --title "The Iranian Integrated Care Electronic Health Record."
```

#### Country-based Co-authorship
A country-based co-authorship network refers to a network of collaborative relationships between researchers from different countries who have co-authored academic papers together. It represents the connections and collaborations that exist among researchers across national boundaries.

By studying a country-based co-authorship network, researchers can gain insights into international collaborations, identify emerging research trends, foster interdisciplinary cooperation, and facilitate policy decisions related to research funding, academic mobility, and scientific development at a global scale.

There are several software tools available that can help you produce country-based co-authorship networks. Here are a few popular options:

[VOSviewer](https://www.vosviewer.com/): VOSviewer is a widely used software tool for constructing and visualizing co-authorship networks. It offers various clustering and visualization techniques and allows you to analyze and explore the network based on different attributes, including country affiliation.

[Sci2 Tool](https://sci2.cns.iu.edu/user/index.php): The Science of Science (Sci2) Tool is a Java-based software package (in [GitHub](https://github.com/CIShell)) that supports the analysis and visualization of scientific networks. It offers a variety of functionalities for constructing and analyzing co-authorship networks, including country-based analysis. It allows users to perform data preprocessing, network analysis, and visualization within a single integrated environment.

To convert affiliation into a hierarchical structure of country, city and centers, you can use the following command:

```shell
python .\triplea\cli\aaa.py pipeline -n FlagAffiliationMining
```


#### Extract Triple from Abstract

```shell
python .\triplea\cli\aaa.py pipeline --name FlagExtractKG
```



#### Extract Topic from Abstract

```shell
python .\triplea\cli\aaa.py pipeline --name FlagExtractTopic
```

An example of working with the functions of this part using `Jupyter` is given in [here](https://github.com/EhsanBitaraf/triple-a/blob/main/cookbook/selection-sampling.ipynb). which is finally drawn using VOSviewer program as below:

![](https://github.com/EhsanBitaraf/triple-a/tree/main/docs/assets/img/topic-graph-biobank.png)

### Import Data

#### Import Single Reference File
Import file type is `.bib` , `.enw` , `.ris`

```shell
python .\triplea\cli\importbib.py "C:\...\bc.ris"
```

output:

![](https://github.com/EhsanBitaraf/triple-a/tree/main/docs/docs/assets/img/import-output.png)


#### Import Triplea Format

```sh
python .\triplea\cli\aaa.py import --help
```


```sh
python .\triplea\cli\aaa.py import --type triplea --format json --bar True "C:\BibliometricAnalysis.json"
```


### Export Data
Various data export can be created from the article repository. These outputs are used to create raw datasets.

|Type|Format|
|-|-|
|triplea|json, csv , *csvs*|
|rayyan|csv|
|RefMan*|ris|


* It has not yet been implemented.


For guidance from the export command, you can act like this:
```sh
python .\triplea\cli\aaa.py export --help
```

For Example :




The export is limited to 100 samples, and the resulting exported articles are saved in the file Triple Json format named "test_export.json".
```sh
python .\triplea\cli\aaa.py export --type triplea --format json --limit 100 --output "test_export.json"
```


```sh
python .\triplea\cli\aaa.py export --type triplea --format json --output "test_export.json"
```

Export Triplea CSV format:
```sh
python .\triplea\cli\aaa.py export --type triplea --format csv --output "test_export.csv"
```


```sh
python .\triplea\cli\aaa.py export --type triplea --format csvs --output "export.csv"
```


Export for Rayyan CSV format:
```sh
python .\triplea\cli\aaa.py export --type rayyan --format csv --output "test_export.csv"
```

### Export Graph

for details information:
```sh
python .\triplea\cli\aaa.py export_graph --help
```


Making a graph with the `graphml` format and saving it in a file `test.graphml`
```shell
python .\triplea\cli\aaa.py export_graph -g gen-all -f graphml -o .\triplea\test
```

Making a graph with the `gexf` format and saving it in a file `C:\Users\Dr bitaraf\Documents\graph\article.gexf`.This graph contains article, author, affiliation and relation between them:
```shell
python .\triplea\cli\aaa.py export_graph -g article-author-affiliation -f gexf -o "C:\Users\Dr bitaraf\Documents\graph\article"
```

Making a graph with the `graphdict` format and saving it in a file `C:\Users\Dr bitaraf\Documents\graph\article.json`.This graph contains article, Reference, article cite and relation between them:
```shell
python .\triplea\cli\aaa.py export_graph -g article-reference -g article-cited -f graphdict -o "C:\Users\Dr bitaraf\Documents\graph\article.json"
```

Making a graph with the `graphml` format and saving it in a file `C:\graph-repo\country-authorship.jgraphmlson`.This graph contains article, country, and relation between them:
```shell
python .\triplea\cli\aaa.py export_graph -g country-authorship -f graphml -o "C:\graph-repo\country-authorship"
```


Types of graph generators that can be used in the `-g` parameter:

|Name|Description|
|----|-----------|
|store|It considers all the nodes and edges that are stored in the database|
|gen-all|It considers all possible nodes and edges|
|article-topic|It considers article and topic as nodes and edges between them|
|article-author-affiliation|It considers article, author and affiliation as nodes and edges between them|
|article-keyword|It considers article and keyword as nodes and edges between them|
|article-reference|It considers article and reference as nodes and edges between them|
|article-cited|It considers article and cited as nodes and edges between them|
|country-authorship||

Types of graph file format that can be used in the `-f` parameter:
|Name|Description|
|----|-----------|
|graphdict|This format is a customized format for citation graphs in the form of a Python dictionary.|
|graphjson||
|gson||
|gpickle|Write graph in Python pickle format. Pickles are a serialized byte stream of a Python object|
|graphml|The GraphML file format uses .graphml extension and is XML structured. It supports attributes for nodes and edges, hierarchical graphs and benefits from a flexible architecture.|
|gexf|GEXF (Graph Exchange XML Format) is an XML-based file format for storing a single undirected or directed graph.|

### Visualizing Graph
Several visualizator are used to display graphs in this program. These include:

[Alchemy.js](https://graphalchemist.github.io/Alchemy/#/) : Alchemy.js is a graph drawing application built almost entirely in d3.

[interactivegaraph](https://github.com/grapheco/InteractiveGraph) : InteractiveGraph provides a web-based interactive visualization and analysis framework for large graph data, which may come from a GSON file

[netwulf](https://github.com/benmaier/netwulf) : Interactive visualization of networks based on Ulf Aslak's d3 web app.


```shell
python .\triplea\cli\aaa.py visualize -g article-reference -g article-cited -p 8001
```


```shell
python .\triplea\cli\aaa.py visualize -g gen-all -p 8001
```


output:

![](https://github.com/EhsanBitaraf/triple-a/tree/main/docs/docs/assets//img/gen-all-graph.png)


```shell
python .\triplea\cli\aaa.py visualize -g article-topic -g article-keyword -p 8001
```

output:

![](https://github.com/EhsanBitaraf/triple-a/tree/main/docs/docs/assets/img/graph-alchemy.png)


Visulaize File

A file related to the extracted graph can be visualized in different formats with the following command:
```sh
python .\triplea\cli\aaa.py visualize_file --format graphdict "graph.json"
```

### Analysis Graph


`analysis info` command calculates specific metrics for the entire graph. These metrics include the following:
- Graph Type: 
- SCC: 
- WCC: 
- Reciprocity : 
- Graph Nodes: 
- Graph Edges: 
- Graph Average Degree : 
- Graph Density : 
- Graph Transitivity : 
- Graph max path length : 
- Graph Average Clustering Coefficient : 
- Graph Degree Assortativity Coefficient : 

```
python .\triplea\cli\aaa.py analysis -g gen-all -c info
```

output:

![](https://github.com/EhsanBitaraf/triple-a/tree/main/docs/docs/assets/img/aaa-analysis-info.png)




Creates a graph with all possible nodes and edges and calculates and lists the sorted [degree centrality](https://bookdown.org/omarlizardo/_main/4-2-degree-centrality.html) for each node.
```
python .\triplea\cli\aaa.py analysis -g gen-all -c sdc
```

output:

![](https://github.com/EhsanBitaraf/triple-a/tree/main/docs/docs/assets/img/aaa-analysis-sdc.png)


### Work with Article Repository
Article Repository (Arepo) is a database that stores the information of articles and graphs. Different databases can be used. We have used the following information banks here:

- [TinyDB](https://github.com/msiemens/tinydb) - TinyDB is a lightweight document oriented database

- [MongoDB](https://www.mongodb.com/) - MongoDB is a source-available cross-platform document-oriented database program


To get general information about the articles, nodes and egdes in the database, use the following command.
```shell
python .\triplea\cli\aaa.py arepo -c info
```

output:
```shell
Number of article in article repository is 122
0 Node(s) in article repository.
0 Edge(s) in article repository.
122 article(s) in state 3.
```



Get article data by PMID
```sh
python .\triplea\cli\aaa.py arepo -pmid 31398071
```

output:
```
Title   : Association between MRI background parenchymal enhancement and lymphovascular invasion and estrogen receptor status in invasive breast cancer.
Journal : The British journal of radiology
DOI     : 10.1259/bjr.20190417
PMID    : 31398071
PMC     : PMC6849688
State   : 3
Authors : Jun Li, Yin Mo, Bo He, Qian Gao, Chunyan Luo, Chao Peng, Wei Zhao, Yun Ma, Ying Yang, 
Keywords: Adult, Aged, Breast Neoplasms, Female, Humans, Lymphatic Metastasis, Magnetic Resonance Imaging, Menopause, Middle Aged, Neoplasm Invasiveness, Receptors, Estrogen, Retrospective Studies, Young Adult,
```

Get article data by PMID and save to `article.json` file.
```sh
python .\triplea\cli\aaa.py arepo -pmid 31398071 -o article.json
```

another command fo this:
```sh
python .\triplea\cli\aaa.py export_article --idtype pmid --id 31398071 --format json --output "article.json"
```

### Configuration

For details information:
```shell
python .\triplea\cli\aaa.py config --help
```

Get environment variable:
```shell
 python .\triplea\cli\aaa.py config -c info
```

Set new environment variable:
```shell
python .\triplea\cli\aaa.py config -c update
```

Below is a summary of important environment variables in this project:
|Environment Variables     |Description|Default Value|
|--------------------------|-----------|-------------|
|TRIPLEA_DB_TYPE           |The type of database to be used in the project. The database layer is separate and you can use different databases, currently it supports `MongoDB` and `TinyDB` databases. TinyDB can be used for small scope and Mango can be used for large scope|TinyDB|
|AAA_TINYDB_FILENAME       |File name of TinyDB|articledata.json|
|AAA_MONGODB_CONNECTION_URL|[Standard Connection String Format](https://www.mongodb.com/docs/manual/reference/connection-string/#std-label-connections-standard-connection-string-format) For MongoDB|mongodb://user:pass@127.0.0.1:27017/|
|AAA_MONGODB_DB_NAME       |Name of MongoDB Collection|articledata|
|AAA_TPS_LIMIT             |Transaction Per Second Limitation|1|
|AAA_PROXY_HTTP            |An HTTP proxy is a server that acts as an intermediary between a client and PubMed server. When a client sends a request to a server through an HTTP proxy, the proxy intercepts the request and forwards it to the server on behalf of the client. Similarly, when the server responds, the proxy intercepts the response and forwards it back to the client.||
|AAA_PROXY_HTTPS           |HTTPS Proxy|| 
|AAA_CLIENT_AGENT          |||
|AAA_REFF_CRAWLER_DEEP     ||1|
|AAA_CITED_CRAWLER_DEEP    ||1|
|AAA_CLI_ALERT_POINT||500|
|AAA_TOPIC_EXTRACT_ENDPOINT|||
|AAA_SCIGENIUS_ENDPOINT|||
|AAA_LLM_TEMPLATE_FILE|||
|AAA_FULL_TEXT_REPO_TYPE|||
|AAA_FULL_TEXT_DIRECTORY|||
|AAA_FULL_TEXT_STRING_REPO_TYPE|||
|AAA_FULL_TEXT_STRING_DIRECTORY|||



# Testing

To ensure the functionality and reliability of the application, you can run tests using **pytest**. Follow the steps below to execute the tests:

## Running All Tests

To run all tests in the project, use the following command:

```sh
poetry run pytest
```

This command will discover and execute all test files and functions within your project directory.

## Running Tests in a Specific Directory

If you want to run tests that are specifically located in a designated directory (e.g., the `tests/` directory), you can specify that directory as follows:

```sh
poetry run pytest tests/
```

This command will only execute the tests found within the specified `tests/` directory.

## Running Tests with Coverage

To measure test coverage, you can use the `--cov` option. This will report which parts of your code are covered by tests:

```sh
poetry run pytest --cov
```

This command provides a summary of code coverage in the terminal, allowing you to identify untested areas of your code.

## Additional Coverage Reports

If you would like to generate a more detailed coverage report in HTML format, you can add the following command after running the tests:

```sh
poetry run pytest --cov --cov-report html
```

This will create a directory named `htmlcov` containing an HTML report, which you can open in your web browser to visually inspect coverage details.


# Dependencies

The project relies on various libraries for different functionalities. Below is a categorized list of dependencies required for the project:

## Graph Analysis
- [**networkx**](https://networkx.org/): A library for creating, manipulating, and studying the structure and dynamics of complex networks.

## Natural Language Processing (NLP)
- [**PyTextRank**](https://derwen.ai/docs/ptr/): A library for keyword extraction and summarization using graph-based ranking algorithms.
- [**transformers**](https://huggingface.co/docs/transformers/index): A state-of-the-art library for natural language processing tasks, providing pre-trained models for various NLP applications.
- [**spaCy**](https://spacy.io/): An advanced NLP library designed for production use, offering efficient and easy-to-use tools for text processing.

## Data Storage
- [**TinyDB**](https://tinydb.readthedocs.io/en/latest/): A lightweight document-oriented database that stores data in JSON format, suitable for small projects.
- [**py2neo**](https://github.com/py2neo-org/py2neo): A client library for working with Neo4j graph databases, allowing for easy manipulation of graph data.
- [**pymongo**](https://github.com/mongodb/mongo-python-driver): The official Python driver for MongoDB, providing a way to interact with MongoDB databases.

## Visualization of Networks
- [**netwulf**](https://github.com/benmaier/netwulf): A library for visualizing networks directly in the browser, designed for interactive exploration of network data.
- [**Alchemy.js**](https://graphalchemist.github.io/Alchemy/#/): A JavaScript library for visualizing networks with an emphasis on aesthetics and interaction.
- [**InteractiveGraph**](https://github.com/grapheco/InteractiveGraph): A framework for creating interactive graph visualizations, enabling users to explore graph data dynamically.

## Command-Line Interface (CLI)
- [**click**](https://click.palletsprojects.com/en/8.1.x/): A Python package for creating command-line interfaces with a focus on ease of use and flexibility.

## Packaging and Dependency Management
- [**Poetry**](https://python-poetry.org/docs/basic-usage/): A dependency management and packaging tool that simplifies the management of Python projects and their dependencies.





# Use Case

This tool allows you to create datasets in various formats. Below are examples of how to use the tool for creating a dataset related to breast cancer research.

## Breast Cancer Dataset

### PubMed Query
To gather relevant articles, use the following PubMed query:
```
"breast neoplasms"[MeSH Terms] OR ("breast"[All Fields] AND "neoplasms"[All Fields]) OR "breast neoplasms"[All Fields] OR ("breast"[All Fields] AND "cancer"[All Fields]) OR "breast cancer"[All Fields]
```

This query returns `495,012` results.

### Configuration
Before running the tool, ensure your configuration settings are properly defined in your environment variables:
```plaintext
AAA_MONGODB_DB_NAME = bcarticledata
AAA_REFF_CRAWLER_DEEP = 0
AAA_CITED_CRAWLER_DEEP = 0
```
*Note: The `EDirect` tool is used for fetching articles from PubMed.*

### Search Command
You can initiate the search using the following command:
```bash
python .\triplea\cli\aaa.py search --searchterm r'"breast neoplasms"[MeSH Terms] OR ("breast"[All Fields] AND "neoplasms"[All Fields]) OR "breast neoplasms"[All Fields] OR ("breast"[All Fields] AND "cancer"[All Fields]) OR "breast cancer"[All Fields]'
```

If the `--searchterm` argument is too complex, you can run the search without it:
```bash
python .\triplea\cli\aaa.py search
```

### Filtering Results
You can filter the search results based on publication date using the following filter criteria:
```json
{
    "mindate": "2022/01/01",
    "maxdate": "2022/12/30"
}
```

### Retrieving Downloaded Article Information
To get an overview of all downloaded articles, run:
```bash
python .\triplea\cli\aaa.py arepo -c info
```
The output will provide details like this:
```plaintext
Number of articles in article repository: 30,914
0 Node(s) in article repository.
0 Edge(s) in article repository.
30,914 article(s) in state 0.
```

### Advancing Article States
To move the articles through different processing states, execute the following commands:

1. **Run the core pipeline to advance from state 0 to state 1:**
    ```bash
    python .\triplea\cli\aaa.py next --state 0
    ```

2. **Parse articles from state 1 to state 2:**
    ```bash
    python .\triplea\cli\aaa.py next --state 1
    ```

### Custom Pipeline for Extracting Triples
To extract triples from the articles using a custom pipeline, run:
```bash
python .\triplea\cli\aaa.py pipeline --name FlagExtractKG
```



## Bio-Bank Dataset

### PubMed Query
To gather articles related to biological specimen banks, use the following PubMed query:
```
"Biological Specimen Banks"[Mesh] OR BioBanking OR biobank OR dataBank OR "Bio Banking" OR "bio bank"
```

This query returns a total of `39,023` results.

### Search Command
You can initiate the search using the following command:
```bash
python .\triplea\cli\aaa.py search --searchterm "\"Biological Specimen Banks\"[Mesh] OR BioBanking OR biobank OR dataBank OR \"Bio Banking\" OR \"bio bank\""
```

### Handling Query Limitations
When querying PubMed, if the number of results exceeds `10,000`, you may encounter an error similar to this:
```
"ERROR":"Search Backend failed: Exception:\n\'retstart\' cannot be larger than 9998. For PubMed, ESearch can only retrieve the first 9,999 records matching the query. To obtain more than 9,999 PubMed records, consider using EDirect, which contains additional logic to batch PubMed search results automatically."
```

PubMed's ESearch can only retrieve the first `10,000` records. To gather more than `10,000` UIDs, consider submitting multiple ESearch requests while incrementing the `retstart` value. For detailed instructions, refer to the [EDirect documentation](https://www.ncbi.nlm.nih.gov/books/NBK25499/).

This limitation is hardcoded in the `get_article_list_from_pubmed` method in `PARAMS`.

### Additional Query
A more recent query was added to refine the search:
```
"bio-banking"[Title/Abstract] OR "bio-bank"[Title/Abstract] OR "data-bank"[Title/Abstract]
```
This query returns an additional `9,012` results.

You can run this query using the following command:
```bash
python .\triplea\cli\aaa.py search --searchterm "\"bio-banking\"[Title/Abstract] OR \"bio-bank\"[Title/Abstract] OR \"data-bank\"[Title/Abstract]"
```

### Retrieve Article Information
After running the above search, you can check the number of articles in the repository with:
```
Number of articles in article repository: 47,735
```

### Exporting Data
To export the dataset in `graphml` format, execute the following command:
```bash
python .\triplea\cli\aaa.py export_graph -g article-reference -g article-keyword -f graphml -o .\triplea\datasets\biobank.graphml
```

## Registry of Breast Cancer Dataset

### Keyword Checking
To ensure comprehensive coverage of breast cancer research, the following keywords were verified:
```
"Breast Neoplasms"[Mesh]  
"Breast Cancer"[Title]  
"Breast Neoplasms"[Title]  
"Breast Neoplasms"[Other Term]  
"Breast Cancer"[Other Term]  
"Registries"[Mesh]  
"Database Management Systems"[Mesh]  
"Information Systems"[MeSH Major Topic]  
"Registries"[Other Term]  
"Information Storage and Retrieval"[MeSH Major Topic]  
"Registry"[Title]  
"National Program of Cancer Registries"[Mesh]  
"Registries"[MeSH Major Topic]  
"Information Science"[Mesh]  
"Data Management"[Mesh]  
```

### Final PubMed Query
Based on the above keywords, the final PubMed query is constructed as follows:
```plaintext
("Breast Neoplasms"[Mesh] OR "Breast Cancer"[Title] OR "Breast Neoplasms"[Title] OR "Breast Neoplasms"[Other Term] OR "Breast Cancer"[Other Term]) AND ("Registries"[MeSH Major Topic] OR "Database Management Systems"[MeSH Major Topic] OR "Information Systems"[MeSH Major Topic] OR "Registry"[Other Term] OR "Registry"[Title] OR "Information Storage and Retrieval"[MeSH Major Topic])
```

### Query URL
You can execute this query directly using the following URL:
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=("Breast+Neoplasms"[Mesh]+OR+"Breast+Cancer"[Title]+OR+"Breast+Neoplasms"[Title]+OR+"Breast+Neoplasms"[Other+Term]+OR+"Breast+Cancer"[Other+Term])+AND+("Registries"[MeSH+Major+Topic]+OR+"Database+Management+Systems"[MeSH+Major+Topic]+OR+"Information+Systems"[MeSH+Major+Topic]+OR+"Registry"[Other+Term]+OR+"Registry"[Title]+OR+"Information+Storage+and+Retrieval"[MeSH+Major+Topic])&retmode=json&retstart=1&retmax=10
```

### Downloading Dataset
You can download the results of this network, which include the relationships between articles and keywords, in `graphdict` format from the following link:
- [Download graphdict format](https://github.com/EhsanBitaraf/triple-a/tree/main/datasets/bcancer-graphdict.json)

If you prefer to work with the graph in `graphml` format, you can download it here:
- [Download graphml format](https://github.com/EhsanBitaraf/triple-a/tree/main/datasets/bcancer.graphml)



# Public Dataset

This section provides access to several datasets produced using this program. These datasets have been structured in a simpler format compared to the program's internal database, enhancing usability for researchers and practitioners. You can utilize the `export_engine` function to obtain outputs tailored to your preferred structure. For a simple example of how to use this function, please refer to the [sample export engine script](https://github.com/EhsanBitaraf/triple-a/blob/main/cookbook/sample-export-engine-simple.py).

## Topic Extraction Dataset - Related to Breast Cancer Therapy

This dataset comprises a total of **9,691 articles** from the medical domain, specifically focused on breast cancer therapy. Topic extraction was performed using two distinct methodologies: **TextRank** and **LLM** (Large Language Models). These approaches leveraged the keywords found within the articles to generate the dataset for analysis. The dataset includes various fields, such as:

- Article title
- Publication year
- PMID (PubMed Identifier)
- Keyword listings
- Topics derived through the TextRank algorithm
- Topics identified through LLM analysis

**License:**  
*MIT*

**DOI:** [10.6084/m9.figshare.25533532.v1](https://doi.org/10.6084/m9.figshare.25533532.v1)

---

## Coronary Artery Disease Clinical Trial Articles

This collection consists of articles related to clinical trials on **coronary artery disease**, featuring the following information for each article:

- Year of publication
- Title
- Abstract
- PMID (PubMed Identifier)

These articles were extracted from the PubMed database using a specific search strategy designed to capture relevant clinical trial information.

**License:**  
*CC BY 4.0*

**DOI:** [10.6084/m9.figshare.26116768.v2](https://doi.org/10.6084/m9.figshare.26116768.v2)

---

## MIE Articles Dataset

The MIE Articles Dataset contains **4,606 articles** presented at the **Medical Informatics Europe Conference** (MIE) from **1996 to 2024**. This data was extracted from PubMed, and topic extraction as well as affiliation parsing were conducted on the dataset.

**License:**  
*CC BY 4.0*

**DOI:** [10.6084/m9.figshare.27174759.v1](https://doi.org/10.6084/m9.figshare.27174759.v1)



# Graph Visualization 
Various tools have been developed to visualize graphs. We have done a [brief review](docs/graph-visualization.md) and selected a few tools to use in this program.

# Graph Analysis
In this project, we used one of the most powerful libraries for graph analysis. Using [NetworkX](https://networkx.org/), we generated many indicators to check a citation graph. Some materials in this regard are given [here](docs/graph-analysis.md). You can use other libraries as well.


# Knowledge Extraction
In the architecture of this software, the structure of the article is stored in the database and this structure also contains the summary of the article. For this reason, it is possible to perform NLP processes such as keywords extraction, topic extraction etc., which can be completed in the future[.](docs/knowledge-extraction.md)


# Related Article
This topic is very interesting from a research point of view, so I have included the articles that were interesting [here](docs/article.md).



# Code Quality
We used flake8 and black libraries to increase code quality.
More information can be found [here](docs/code-quality.md).

---

# Citation

If you use `Triple A` for your scientific work, consider citing us! We're published in [IEEE](https://ieeexplore.ieee.org/document/10139229).

```bibtex
@INPROCEEDINGS{10139229,
  author={Jafarpour, Maryam and Bitaraf, Ehsan and Moeini, Ali and Nahvijou, Azin},
  booktitle={2023 9th International Conference on Web Research (ICWR)}, 
  title={Triple A (AAA): a Tool to Analyze Scientific Literature Metadata with Complex Network Parameters}, 
  year={2023},
  volume={},
  number={},
  pages={342-345},
  doi={10.1109/ICWR57742.2023.10139229}}
```

[![DOI:10.1109/ICWR57742.2023.10139229](https://zenodo.org/badge/doi/10.1109/ICWR57742.2023.10139229.svg)](https://doi.org/10.1109/ICWR57742.2023.10139229)



---

# License

TripleA is available under the [Apache License](LICENSE).



