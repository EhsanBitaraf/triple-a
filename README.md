# triple-a
*Article Analysis Assistant*

This program somehow creates a network of article references and provides a connection between authors and keywords, these things are usually called "[**Citation Graph**](https://en.wikipedia.org/wiki/Citation_graph)".

There are various software and online systems for this, a brief review of which can be found [here](docs/related-work.md).

This tool gives you the power to create a graph of articles and analyze it. This tool is designed as a **CLI** (command-line interface) and you can use it as a Python library.

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub Last commit](https://img.shields.io/github/last-commit/EhsanBitaraf/triple-a)](https://github.com/EhsanBitaraf/triple-a/main)
[![commits](https://badgen.net/github/commits/EhsanBitaraf/triple-a/main)](https://github.com/EhsanBitaraf/triple-a/commits/main?icon=github&color=green)
![Release](https://img.shields.io/github/release/EhsanBitaraf/triple-a)
![repo size](https://img.shields.io/github/repo-size/EhsanBitaraf/triple-a)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/EhsanBitaraf/triple-a)
![Open Issue](https://img.shields.io/github/issues-raw/EhsanBitaraf/triple-a)
[![GitHub tag](https://img.shields.io/github/tag/EhsanBitaraf/triple-a.svg)](https://GitHub.com/EhsanBitaraf/triple-a/tags/)
![Downloads](https://img.shields.io/github/downloads/EhsanBitaraf/triple-a/total)

![Build and push images](https://github.com/EhsanBitaraf/triple-a/workflows/push%20docker%20image/badge.svg)

![Testing](https://github.com/EhsanBitaraf/triple-a/actions/workflows/test-poetry-action.yml/badge.svg)

![Code Quality](https://github.com/EhsanBitaraf/triple-a/actions/workflows/python-flake.yml/badge.svg)

<!-- ![Release](https://img.shields.io/github/release-date/EhsanBitaraf/triple-a) -->

<!-- ![PyPI - Wheel](https://img.shields.io/pypi/EhsanBitaraf/triple-a) -->

<!-- test this :

https://badge.fury.io/for/py/Triple-a -->

<!-- [![GitHub commits](https://img.shields.io/github/commits-since/EhsanBitaraf/triple-a/v1.0.0.svg)](https://github.com/EhsanBitaraf/triple-a/commit/master) -->



- [🎮 Main Features](#---main-features)
- [How to use](#how-to-use)
  * [Setup](#setup)
  * [Functional Use](#functional-use)
    + [Training NER for Article Title](#training-ner-for-article-title)
  * [Command Line (CLI) Use](#command-line--cli--use)
    + [Get and Save list of article identifier base on search term](#get-and-save-list-of-article-identifier-base-on-search-term)
    + [Move core pipeline state](#move-core-pipeline-state)
    + [Run custom pipeline](#run-custom-pipeline)
      - [NER Article Title](#ner-article-title)
      - [Country-based Co-authorship](#country-based-co-authorship)
      - [Extract Triple from Abstract](#extract-triple-from-abstract)
      - [Extract Topic from Abstract](#extract-topic-from-abstract)
    + [Import Single Reference File](#import-single-reference-file)
    + [Export graph](#export-graph)
    + [Visualizing Graph](#visualizing-graph)
    + [Analysis Graph](#analysis-graph)
    + [Work with Article Repository](#work-with-article-repository)
    + [Configuration](#configuration)
- [Testing](#testing)
- [Dependencies](#dependencies)
- [Use case](#use-case)
  * [Bio Bank](#bio-bank)
  * [Registry of Breast Cancer](#registry-of-breast-cancer)
  * [EHR](#ehr)
- [Graph Visualization](#graph-visualization)
- [Graph Analysis](#graph-analysis)
- [Knowledge Extraction](#knowledge-extraction)
- [Related Article](#related-article)
- [Code Quality](#code-quality)
- [Citation](#citation)
- [License](#license)





# 🎮 Main Features
- Single paper analysis
- Dynamic citations deep definition for meta data fetch
- Network Analysis (Per Node/Overall Graph)
- Import bibliography file
- Use for [Bibliometric Analysis](https://researchguides.uic.edu/bibliometrics)



# How to use 

## Setup

Clone repository:
```shell
git clone https://github.com/EhsanBitaraf/triple-a.git
```

or 

```shell
git clone git@github.com:EhsanBitaraf/triple-a.git
```

Create environment variable:
```shell
python -m venv venv
```

Activate environment variable:

*Windows*
```shell
$ .\venv\Scripts\activate
```

*Linux*
```shell
$ source venv/bin/activate
```

Install poetry:
```shell
pip install poetry
```

Instal dependences:
```shell
poetry install
```

run cli:
```shell
poetry run python triplea/cli/aaa.py 
```

## Functional Use

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

open befor file for debuging use
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

### Training NER for Article Title

You can use NLP(Natural Language Processing) methods to extract information from the structure of the article and add it to your graph. For example, you can extract NER(Named-entity recognition) words from the title of the article and add to the graph. [Here's how to create a custom NER](docs/training-ner.md).



## Command Line (CLI) Use

By using the following command, you can see the command completion `help`. Each command has a separate `help`.

```shell
python .\triplea\cli\aaa.py  --help
```

output:

![](docs/assets/img/aaa-help.png)


### Get and Save list of article identifier base on search term

Get list of article identifier (PMID) base on search term and save into knowledge repository in first state (0):

use this command:
```shell
python .\triplea\cli\aaa.py search --searchterm [searchterm]
```

Even the PMID itself can be used in the search term.
```shell
python .\triplea\cli\aaa.py search --searchterm 36467335
```

output:

![](docs/assets/img/aaa-search.png)

### Move core pipeline state
The preparation of the article for extracting the graph has different steps that are placed in a pipeline. Each step is identified by a number in the state value. The following table describes the state number:

*List of state number*

|State|Description|
|-|-|
|0|article identifier saved|
|1|article details article info saved (json Form)|
|2|parse details info|
|3|Get Citation|
|4|NER Title|
|5|extract graph|
|-1|Error|


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

![](docs/assets/img/aaa-next.png)


`go` command:
```shell
python .\triplea\cli\aaa.py go --end [last state]
```

```shell
python .\triplea\cli\aaa.py go --end 3
```

output:

![](docs/assets/img/aaa-go.png)


### Run custom pipeline
Apart from the core pipelines that should be used to prepare articles, customized pipelines can also be used. Custom pipelines may be implemented to extract knowledge from texts and NLP processing. These pipelines themselves can form a new graph other than the citation graph or in combination with it.


List of Custom Pipeline

|Action|Tag Name|Description|
|------|--------|-----------|
|Triple extraction from article abstract|FlagExtractKG||
|Topic extraction from article abstract|FlagExtractTopic||
|Convert Affiliation text to structural data|FlagAffiliationMining|This is simple way for parse Affiliation text |
|Convert Affiliation text to structural data|FlagAffiliationMining_Titipata|use [Titipat Achakulvisut Repo](https://github.com/titipata/affiliation_parser) for parsing Affiliation text|

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

An example of working with the functions of this part using `Jupyter` is given in [here](./jupyter_lab/selection-sampling.ipynb). which is finally drawn using VOSviewer program as below:

![](./docs/assets/img/topic-graph-biobank.png)

### Import Data

#### Import Single Reference File
Import file type is `.bib` , `.enw` , `.ris`

```shell
python .\triplea\cli\importbib.py "C:\...\bc.ris"
```

output:

![](docs/assets/img/import-output.png)


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

![](docs/assets//img/gen-all-graph.png)


```shell
python .\triplea\cli\aaa.py visualize -g article-topic -g article-keyword -p 8001
```

output:

![](docs/assets/img/graph-alchemy.png)


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

![](docs/assets/img/aaa-analysis-info.png)




Creates a graph with all possible nodes and edges and calculates and lists the sorted [degree centrality](https://bookdown.org/omarlizardo/_main/4-2-degree-centrality.html) for each node.
```
python .\triplea\cli\aaa.py analysis -g gen-all -c sdc
```

output:

![](docs/assets/img/aaa-analysis-sdc.png)


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
|AAA_REFF_CRAWLER_DEEP     ||1|
|AAA_CITED_CRAWLER_DEEP    ||1|

# Testing

```sh
poetry run pytest
```

```sh
poetry run pytest --cov
```


For unit test check :

bibilometric:

37283018

35970485

# Dependencies



For graph analysis:

[networkx](https://networkx.org/)


For NLP:

[PyTextRank](https://derwen.ai/docs/ptr/)

[transformers](https://huggingface.co/docs/transformers/index) 

[spaCy](https://spacy.io/)

For data storage:
 
[TinyDB](https://tinydb.readthedocs.io/en/latest/)

[py2neo](https://github.com/py2neo-org/py2neo)

[pymongo](https://github.com/mongodb/mongo-python-driver)

For visualization of networks:

[netwulf](https://github.com/benmaier/netwulf)

[Alchemy.js](https://graphalchemist.github.io/Alchemy/#/)

[InteractiveGraph](https://github.com/grapheco/InteractiveGraph)

For CLI:

[click](https://click.palletsprojects.com/en/8.1.x/)


For packaging and dependency management: 

[Poetry](https://python-poetry.org/docs/basic-usage/)



# Use case
With this tool, you can create datasets in different formats, here are examples of these datasets.


## Breast Cancer

Pubmed Query:
```
"breast neoplasms"[MeSH Terms] OR ("breast"[All Fields] AND "neoplasms"[All Fields]) OR "breast neoplasms"[All Fields] OR ("breast"[All Fields] AND "cancer"[All Fields]) OR "breast cancer"[All Fields]
```

`495,012` results

Configuration:
```
AAA_MONGODB_DB_NAME = bcarticledata
AAA_REFF_CRAWLER_DEEP = 0
AAA_CITED_CRAWLER_DEEP = 0
```

`EDirect` used.

Search with this command:

```
python .\triplea\cli\aaa.py search --searchterm r'"breast neoplasms"[MeSH Terms] OR ("breast"[All Fields] AND "neoplasms"[All Fields]) OR "breast neoplasms"[All Fields] OR ("breast"[All Fields] AND "cancer"[All Fields]) OR "breast cancer"[All Fields]'
```

if --searchterm argument is too complex use this:
```
python .\triplea\cli\aaa.py search
```

by Filter :
```
{
    "mindate" : "2022/01/01",
    "maxdate" : "2022/12/30"
}
```

Get info of all downloaded article:
```shell
python .\triplea\cli\aaa.py arepo -c info
```

output:
```shell
Number of article in article repository is 30914
0 Node(s) in article repository.
0 Edge(s) in article repository.
30914 article(s) in state 0.
```

Run Core pipeline to next status
```shell
python .\triplea\cli\aaa.py next --state 0
```

then parsing article:
```shell
python .\triplea\cli\aaa.py next --state 1
```

Extract Triple is type of custom pipeline. you can run this:
```shell
python .\triplea\cli\aaa.py pipeline --name FlagExtractKG
```

## Bio Bank

Pubmed Query:
```
"Biological Specimen Banks"[Mesh] OR BioBanking OR biobank OR dataBank OR "Bio Banking" OR "bio bank"
```

`39,023` results 

Search with this command:

```shell
python .\triplea\cli\aaa.py search --searchterm "\"Biological Specimen Banks\"[Mesh] OR BioBanking OR biobank OR dataBank OR \"Bio Banking\" OR \"bio bank\" "
```

Get 39,023 result until `2023/01/02`

```
"ERROR":"Search Backend failed: Exception:\n\'retstart\' cannot be larger than 9998. For PubMed, ESearch can only retrieve the first 9,999 records matching the query. To obtain more than 9,999 PubMed records, consider using EDirect that contains additional logic to batch PubMed search results automatically so that an arbitrary number can be retrieved. For details see https://www.ncbi.nlm.nih.gov/books/NBK25499/"
```

This query had more than 10,000 results, and as a result, the following text was used:

To retrieve more than 10,000 UIDs from databases other than PubMed, submit multiple esearch requests while incrementing the value of retstart (see Application 3). For PubMed, ESearch can only retrieve the first 10,000 records matching the query. To obtain more than 10,000 PubMed records, consider using `<EDirect>` that contains additional logic to batch PubMed search results automatically so that an arbitrary number can be retrieved.

This is hard code in `get_article_list_from_pubmed` methods in `PARAMS`.

This Query Added lately:
```
"bio-banking"[Title/Abstract] OR "bio-bank"[Title/Abstract] OR "data-bank"[Title/Abstract]
```

`9,012` results

```shell
python .\triplea\cli\aaa.py search --searchterm " \"bio-banking\"[Title/Abstract] OR \"bio-bank\"[Title/Abstract] OR \"data-bank\"[Title/Abstract] "
```

after run this. get info:
```
Number of article in article repository is 47735
```

Export `graphml` format:
```shell
python .\triplea\cli\aaa.py export_graph -g article-reference -g article-keyword  -f graphml -o .\triplea\datasets\biobank.graphml
```

## Registry of Breast Cancer

Keyword Checking:
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

Final Pubmed Query:
```
("Breast Neoplasms"[Mesh] OR "Breast Cancer"[Title] OR "Breast Neoplasms"[Title] OR "Breast Neoplasms"[Other Term] OR "Breast Cancer"[Other Term]) AND ("Registries"[MeSH Major Topic] OR "Database Management Systems"[MeSH Major Topic] OR "Information Systems"[MeSH Major Topic] OR "Registry"[Other Term] OR "Registry"[Title] OR "Information Storage and Retrieval"[MeSH Major Topic])
```

url:
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=("Breast+Neoplasms"[Mesh]+OR+"Breast+Cancer"[Title]+OR+"Breast+Neoplasms"[Title]+OR+"Breast+Neoplasms"[Other+Term]+OR+"Breast+Cancer"[Other+Term])+AND+("Registries"[MeSH+Major+Topic]+OR+"Database+Management+Systems"[MeSH+Major+Topic]+OR+"Information+Systems"[MeSH+Major+Topic]+OR+"Registry"[Other+Term]+OR+"Registry"[Title]+OR+"Information+Storage+and+Retrieval"[MeSH+Major+Topic])&retmode=json&retstart=1&retmax=10
```


You can download the result of this network and the relationship between the article and the keyword in `graphdict` format from [**here**](datasets/bcancer-graphdict.json). Manipulated, you can download this graph in `gramphml` format from [**here**](datasets/bcancer.graphml).

## EHR
It is not yet complete.

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



