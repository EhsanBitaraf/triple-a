# triple-a
*Article Analysis Assistant*

This program somehow creates a network of article references and provides a connection between authors and keywords, these things are usually called "[**Citation Graph**](https://en.wikipedia.org/wiki/Citation_graph)".

There are various software and online systems for this, a brief review of which can be found [here](docs/related-work.md).

This tool gives you the power to create a graph of articles and analyze it. This tool is designed as a **CLI** (command-line interface) and you can use it as a Python library.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![GitHub commit](https://img.shields.io/github/last-commit/EhsanBitaraf/triple-a)](https://github.com/EhsanBitaraf/triple-a/main)
[![Release](https://img.shields.io/github/release/EhsanBitaraf/triple-a.svg?style=flat)]()
 🎮 **Features**

# How to use 

## Setup

Clone repository:
```
git clone https://github.com/EhsanBitaraf/triple-a.git
```

or 

```
git clone git@github.com:EhsanBitaraf/triple-a.git
```

Create environment variable:
```
python -m venv venv
```

Activate environment variable:

*Windows*
```
.\venv\Scripts\activate
```

*Linux*
```
$ source venv/bin/activate
```

Install poetry:
```
pip install poetry
```

Instal dependences:
```
poetry install
```

run cli:
```
poetry run python triplea/cli/aaa.py 
```


## Functional Use

get list of PMID in state 0
```
term = '("Electronic Health Records"[Mesh]) AND ("National"[Title/Abstract]) AND Iran'
get_article_list_all_store_to_kg_rep(term)
```

move from state 1
```
move_state_forward(1)
```

get list of PMID in state 0 and save to file for debugginf use
```
    data = get_article_list_from_pubmed(1, 10,'("Electronic Health Records"[Mesh]) AND ("National"[Title/Abstract])')
    data = get_article_list_from_pubmed(1, 10,'"Electronic Health Records"')
    data1= json.dumps(data, indent=4)
    with open("sample1.json", "w") as outfile:
        outfile.write(data1)
```

open befor file for debuging use
```
    f = open('sample1.json')
    data = json.load(f)
    f.close()
```

get one article from kg and save to file
```
    data = get_article_by_pmid('32434767')
    data= json.dumps(data, indent=4)
    with open("one-article.json", "w") as outfile:
        outfile.write(data)
```

Save Title for Annotation
```
    file =  open("article-title.txt", "w", encoding="utf-8")
    la = get_article_by_state(2)
    for a in la:
        try:
            article = Article(**a.copy())
        except:
            pass
        file.write(article.Title  + "\n")
```

### Trainong NER for Article Title

You can use NLP(Natural Language Processing) methods to extract information from the structure of the article and add it to your graph. For example, you can extract NER(Named-entity recognition) words from the title of the article and add to the graph. [Here's how to create a custom NER](docs/training-ner.md).



## Command Line (CLI) Use

By using the following command, you can see the command completion `help`. Each command has a separate `help`.

```
python .\triplea\cli\aaa.py  --help
```

output:

![](docs/assets/img/aaa-help.png)


### Get and Save list of article identifier base on search term

Get list of article identifier (PMID) base on search term and save into knowledge repository in first state (0):

use this command:
```
python .\triplea\cli\aaa.py search --searchterm [searchterm]
```

Even the PMID itself can be used in the search term.
```
python .\triplea\cli\aaa.py search --searchterm 36467335
```

output:

![](docs/assets/img/aaa-search.png)

### Move data pipeline state
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
```
python .\triplea\cli\aaa.py next --state [current state]
```

for example move all article in state 0 to 1:
```
python .\triplea\cli\aaa.py next --state 0
```
output:

![](docs/assets/img/aaa-next.png)


`go` command:
```
python .\triplea\cli\aaa.py go --end [last state]
```

```
python .\triplea\cli\aaa.py go --end 3
```

output:

![](docs/assets/img/aaa-go.png)




### NER Article Title
You can try the NER method to extract the major topic of the article's title by using the following command. This command is independent and is used for testing and is not stored in the Arepo.

```
python .\triplea\cli\ner.py --title "The Iranian Integrated Care Electronic Health Record."
```

### Import single reference file
Import file type is `.bib` , `.enw` , `.ris`

```
python .\triplea\cli\import.py "C:\...\bc.ris"
```

output:

![](docs/assets/img/import-output.png)


### Export graph

for details information:
```
python .\triplea\cli\aaa.py export_graph --help
```


Making a graph with the `graphml` format and saving it in a file `test.graphml`
```
python .\triplea\cli\aaa.py export_graph -g gen-all -f graphml -o .\triplea\test
```

Making a graph with the `gexf` format and saving it in a file `C:\Users\Dr bitaraf\Documents\graph\article.gexf`.This graph contains article, author, affiliation and relation between them:
```
python .\triplea\cli\aaa.py export_graph -g article-author-affiliation -f gexf -o "C:\Users\Dr bitaraf\Documents\graph\article"
```

Making a graph with the `graphdict` format and saving it in a file `C:\Users\Dr bitaraf\Documents\graph\article.json`.This graph contains article, Reference, article cite and relation between them:
```
python .\triplea\cli\aaa.py export_graph -g article-reference -g article-cited -f graphdict -o "C:\Users\Dr bitaraf\Documents\graph\article.json"
```


### Visualizing Graph
Several visualizator are used to display graphs in this program. These include:

[Alchemy.js](https://graphalchemist.github.io/Alchemy/#/) : Alchemy.js is a graph drawing application built almost entirely in d3.

[interactivegaraph](https://github.com/grapheco/InteractiveGraph) : InteractiveGraph provides a web-based interactive visualization and analysis framework for large graph data, which may come from a GSON file

[netwulf](https://github.com/benmaier/netwulf) : Interactive visualization of networks based on Ulf Aslak's d3 web app.


```
python .\triplea\cli\aaa.py visualize -g article-reference -g article-cited -p 8001
```


```
python .\triplea\cli\aaa.py visualize -g gen-all -p 8001
```


output:

![](docs/assets//img/gen-all-graph.png)


```
python .\triplea\cli\aaa.py visualize -g article-topic -g article-keyword -p 8001
```

output:

![](docs/assets/img/graph-alchemy.png)


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
```
python .\triplea\cli\aaa.py arepo -c info
```

output:
```
Number of article in article repository is 122
0 Node(s) in article repository.
0 Edge(s) in article repository.
122 article(s) in state 3.
```



Get article data by PMID
```
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
```
python .\triplea\cli\aaa.py arepo -pmid 31398071 -o article.json
```




# Testing

```
poetry run pytest
```

# Dependencies

[Poetry](https://python-poetry.org/docs/basic-usage/)

[Using Poetry and Click to create a command line application](https://dataewan.com/blog/poetry-python-command-line/)

[How to create and distribute a minimalist CLI tool with Python, Poetry, Click and Pipx](https://medium.com/clarityai-engineering/how-to-create-and-distribute-a-minimalist-cli-tool-with-python-poetry-click-and-pipx-c0580af4c026)

[Python CLI Utilities with Poetry and Typer](https://www.pluralsight.com/tech-blog/python-cli-utilities-with-poetry-and-typer/)

[How To Create An *Actual* CLI From Your Python Project](https://www.linkedin.com/pulse/how-create-actual-cli-from-your-python-project-samuel-lock/)

[4 Steps to Release a CLI in Python](https://chezo.uno/blog/2022-05-21_fastest-way-to-release-python-cli/)

[Build and Test a Command Line Interface with Python, Poetry, Click, and pytest](https://dev.to/bowmanjd/build-a-command-line-interface-with-python-poetry-and-click-1f5k)

[click](https://click.palletsprojects.com/en/8.1.x/)


Hugging Face


pip install transformers[torch]
```
Downloading (…)lve/main/config.json: 100%|████████████████████████████████████████████████████████| 1.42k/1.42k [00:00<00:00, 712kB/s] 
C:\Users\Dr bitaraf\Desktop\MyData\CodeRepo\github\triple-a\venv\lib\site-packages\huggingface_hub\file_download.py:129: UserWarning: `huggingface_hub` cache-system uses symlinks by default to efficiently store duplicated files but your machine does not support them in 
C:\Users\Dr bitaraf\.cache\huggingface\hub. Caching files will still work but in a degraded version that might require more space on your disk. This warning can be disabled by setting the `HF_HUB_DISABLE_SYMLINKS_WARNING` environment variable. For more details, see https://huggingface.co/docs/huggingface_hub/how-to-cache#limitations.
To support symlinks on Windows, you either need to activate Developer Mode or to run Python as an administrator. In order to see activate developer mode, see this article: https://docs.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development      
  warnings.warn(message)
Downloading (…)"pytorch_model.bin";:   1%|▋                                                       | 21.0M/1.63G [00:27<36:47, 727kB/s]
```

# Use case

## EHR

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



# Graph Visualization 
Various tools have been developed to visualize graphs. We have done a [brief review](docs/graph-visualization.md) and selected a few tools to use in this program.


# Graph Analysis

https://www.kaggle.com/code/rahulgoel1106/network-centrality-using-networkx


Understanding Community Detection Algorithms With Python NetworkX

https://memgraph.com/blog/community-detection-algorithms-with-python-networkx


Graph Measures

https://notebook.community/bjedwards/NetworkXTutorial/V.%20Network%20Analysis


removing isolated vertices in networkx

https://stackoverflow.com/questions/48820586/removing-isolated-vertices-in-networkx

## Usefull Link

### Network Analysis Made Simple 
 An introduction to network analysis and applied graph theory using Python and NetworkX 
https://ericmjl.github.io/Network-Analysis-Made-Simple/


### Network Analysis with Python
Petko Georgiev

Computer Laboratory, University of Cambridge

https://www.cl.cam.ac.uk/teaching/1314/L109/tutorial.pdf

### Graph Analysis - I
https://notebook.community/harrymvr/dataminingapp-lectures/Lecture-17/GraphAnalysis-I

### Tutorial 7: Network analysis

https://infovis.fh-potsdam.de/tutorials/infovis7networks.html

### Lightning Network: Some Graph Theory Metrics — Part 2

https://medium.com/analytics-vidhya/lightning-network-some-graph-theory-metrics-part-2-practical-guide-cfc37fb8e047



## cuGraph 
cuGraph - RAPIDS Graph Analytics Library 

https://github.com/rapidsai/cugraph

# Keyword Extraction 

## Keyword Extraction Methods from Documents in NLP
https://www.analyticsvidhya.com/blog/2022/03/keyword-extraction-methods-from-documents-in-nlp/


##  TextRank
Python implementation of TextRank algorithm for automatic keyword extraction and summarization using Levenshtein distance as relation between text units. This project is based on the paper "TextRank: Bringing Order into Text" by Rada Mihalcea and Paul Tarau. https://web.eecs.umich.edu/~mihalcea/papers/mihalcea.emnlp04.pdf 

require
```
python3 -m spacy download en_core_web_sm
```

https://github.com/davidadamojr/TextRank

# Article

[A Survey of Heterogeneous Information Network Analysis](https://ieeexplore.ieee.org/document/7536145)

[Citation Graph Analysis and Alignment between Citation Adjacency and Themes or Topics of Publications in the Area of Disease Control through Social Network Surveillance](https://link.springer.com/chapter/10.1007/978-3-031-07869-9_5)


[Data Citation and the Citation Graph](https://www.researchgate.net/publication/356021438_Data_Citation_and_the_Citation_Graph)

[Enhancing Scientific Papers Summarization with Citation Graph](https://arxiv.org/abs/2104.03057)
[Github](https://github.com/ChenxinAn-fdu/CGSum)


[Citation Networks as a Multi-layer Graph: Link Prediction and Importance Ranking](http://snap.stanford.edu/class/cs224w-2010/proj2010/05_ProjectReport.pdf)

[GraphCite: Citation Intent Classification in Scientific Publications via Graph Embeddings](https://oanabalalau.com/pdf/graphcite.pdf)

[Efficient algorithms for citation network analysis](https://arxiv.org/pdf/cs/0309023.pdf)


---

## License

TripleA is available under the [Apache License](LICENSE).


## Code Quality
help
```
usage: flake8 [options] file file ...

positional arguments:
  filename

options:
  -h, --help            show this help message and exit
  -v, --verbose         Print more information about what is happening in flake8. This option is repeatable and will increase verbosity each time it is        
                        repeated.
  --output-file OUTPUT_FILE
                        Redirect report to a file.
  --append-config APPEND_CONFIG
                        Provide extra config files to parse in addition to the files found by Flake8 by default. These files are the last ones read and so     
                        they take the highest precedence when multiple files provide the same option.
  --config CONFIG       Path to the config file that will be the authoritative config source. This will cause Flake8 to ignore all other configuration files.  
  --isolated            Ignore all configuration files.
  --enable-extensions ENABLE_EXTENSIONS
                        Enable plugins and extensions that are otherwise disabled by default
  --require-plugins REQUIRE_PLUGINS
                        Require specific plugins to be installed before running
  --version             show program's version number and exit
  -q, --quiet           Report only file names, or nothing. This option is repeatable.
  --color {auto,always,never}
                        Whether to use color in output. Defaults to `auto`.
  --count               Print total number of errors to standard output after all other output.
  --exclude patterns    Comma-separated list of files or directories to exclude. (Default: ['.svn', 'CVS', '.bzr', '.hg', '.git', '__pycache__', '.tox',       
                        '.nox', '.eggs', '*.egg'])
  --extend-exclude patterns
                        Comma-separated list of files or directories to add to the list of excluded ones.
  --filename patterns   Only check for filenames matching the patterns in this comma-separated list. (Default: ['*.py'])
  --stdin-display-name STDIN_DISPLAY_NAME
                        The name used when reporting errors from code passed via stdin. This is useful for editors piping the file contents to flake8.
                        (Default: stdin)
  --format format       Format errors according to the chosen formatter (default, pylint, quiet-filename, quiet-nothing) or a format string containing
                        %-style mapping keys (code, col, path, row, text). For example, ``--format=pylint`` or ``--format='%(path)s %(code)s'``. (Default:     
                        default)
  --hang-closing        Hang closing bracket instead of matching indentation of opening bracket's line.
  --ignore errors       Comma-separated list of error codes to ignore (or skip). For example, ``--ignore=E4,E51,W234``. (Default:
                        E121,E123,E126,E226,E24,E704,W503,W504)
  --extend-ignore errors
                        Comma-separated list of error codes to add to the list of ignored ones. For example, ``--extend-ignore=E4,E51,W234``.
  --per-file-ignores PER_FILE_IGNORES
                        A pairing of filenames and violation codes that defines which violations to ignore in a particular file. The filenames can be
                        specified in a manner similar to the ``--exclude`` option and the violations work similarly to the ``--ignore`` and ``--select``       
                        options.
  --max-line-length n   Maximum allowed line length for the entirety of this run. (Default: 79)
  --max-doc-length n    Maximum allowed doc line length for the entirety of this run. (Default: None)
  --indent-size n       Number of spaces used for indentation (Default: 4)
  --select errors       Comma-separated list of error codes to enable. For example, ``--select=E4,E51,W234``. (Default: E,F,W,C90)
  --extend-select errors
                        Comma-separated list of error codes to add to the list of selected ones. For example, ``--extend-select=E4,E51,W234``.
  --disable-noqa        Disable the effect of "# noqa". This will report errors on lines with "# noqa" at the end.
  --show-source         Show the source generate each error or warning.
  --no-show-source      Negate --show-source
  --statistics          Count errors.
  --exit-zero           Exit with status code "0" even if there are errors.
  -j JOBS, --jobs JOBS  Number of subprocesses to use to run checks in parallel. This is ignored on Windows. The default, "auto", will auto-detect the number  
                        of processors available to use. (Default: auto)
  --tee                 Write to stdout and output-file.
  --benchmark           Print benchmark information about this run of Flake8
  --bug-report          Print information necessary when preparing a bug report

mccabe:
  --max-complexity MAX_COMPLEXITY
                        McCabe complexity threshold

pyflakes:
  --builtins BUILTINS   define more built-ins, comma separated
  --doctests            also check syntax of the doctests
  --include-in-doctest INCLUDE_IN_DOCTEST
                        Run doctests only on these files
  --exclude-from-doctest EXCLUDE_FROM_DOCTEST
                        Skip these files when running doctests

Installed plugins: mccabe: 0.7.0, pycodestyle: 2.10.0, pyflakes: 3.0.1
```

Flake8 Rules

https://www.flake8rules.com/

Sample command:

```
flake8 --show-source .\triplea\cli\main.py
```

```
flake8 --show-source .\triplea\cli\aaa.py --ignore F401,W292
```

```
flake8 --show-source .\triplea\cli\ --ignore F401,W292 --max-line-length 150 --output-file cli.flake8
```
```
flake8  .\triplea\cli\ --select  E225,E231 --show-source --output-file cli.txt  --format '%(path)s:%(row)d:'
```

```
flake8  .\triplea\cli\  --output-file cli.txt  --format pylint
```
```
flake8  .\triplea\cli\  --select E251 --output-file cli.txt  --format pylint --show-source
```


flake8  .\triplea\cli\analysis.py   --output-file cli2.txt  --format pylint --show-source --max-line-length 150 
black .\triplea\cli\analysis.py


flake8  .\triplea\cli\  --output-file cli2.txt  --format pylint --show-source --max-line-length 150 
black .\triplea\cli\

