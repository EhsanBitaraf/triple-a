# triple-a
Article Analysis Assistant


# Use 

## Setup

```
python -m venv venv
```

```
.\venv\Scripts\activate
```


```
pip install poetry
```

```
poetry install
```

```
poetry run python triplea/cli/main.py 
```


## Functional Use

get list of PMID in state 0
```
term = '("Electronic Health Records"[Mesh]) AND ("National"[Title/Abstract]) AND Iran'
get_article_list_all_store_to_kg_rep(term)
```

move to state 1
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

# testing

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


# MEDLINE®PubMed® XML Element Descriptions and their Attributes
[THE ELEMENTS AND THEIR ATTRIBUTES IN PUBMEDARTICLESET](https://www.nlm.nih.gov/bsd/licensee/elements_descriptions.html)


## useful link
https://www.ncbi.nlm.nih.gov/books/NBK25500/


https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch


