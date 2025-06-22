# MEDLINE®PubMed® XML Element Descriptions and their Attributes
[THE ELEMENTS AND THEIR ATTRIBUTES IN PUBMEDARTICLESET](https://www.nlm.nih.gov/bsd/licensee/elements_descriptions.html)

## useful link
https://www.ncbi.nlm.nih.gov/books/NBK25500/


https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch

service
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=("Electronic+Health+Records"[Mesh])+AND+("National"[Title/Abstract])&retmode=json&retstart=${esearchresultRetstart}&retmax=10000
```
```
https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=${PMID.0}&retmode=xml
```

### PMC Article Datasets
https://www.ncbi.nlm.nih.gov/pmc/tools/textmining/

### PMC For Developers
PMC hosts a number of important article datasets and makes our APIs and some code available via public code repositories.

https://www.ncbi.nlm.nih.gov/pmc/tools/developers/

https://www.ncbi.nlm.nih.gov/research/bionlp/APIs/BioC-PMC/


#### Citation

http://api.crossref.org/works/10.1179/1942787514y.0000000039

http://api.crossref.org/works/10.1186/s12911-023-02115-5

https://api.citeas.org/product/10.1186/s12911-023-02115-5


#### citeas-api

Get the scholarly citation for any research product: software, preprint, paper, or dataset 

https://github.com/ourresearch/citeas-api


#### elink
https://github.com/biopython/biopython/blob/master/Bio/Entrez/__init__.py

https://www.ncbi.nlm.nih.gov/books/NBK25500/

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi

https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&id=34577062

 Example: Find related articles to PMID 20210808 

 https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&id=20210808&cmd=neighbor_score

 https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&id=35130239

  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/elink.fcgi?dbfrom=pubmed&db=pubmed&id=35130239&retmode=json

pubmed_pubmed_citedin


# arXiv
arXiv is a free distribution service and an open-access archive for nearly 2.4 million scholarly articles in the fields of physics, mathematics, computer science, quantitative biology, quantitative finance, statistics, electrical engineering and systems science, and economics. Materials on this site are not peer-reviewed by arXiv.

https://arxiv.org/

[arXiv Dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv)
arXiv dataset and metadata of 1.7M+ scholarly papers across STEM

## arXiv API Access

arXiv offers public API access in order to maximize its openness and interoperability. Many projects utilize this option without becoming official [arXivLabs collaborations](https://labs.arxiv.org/).

## arXivLabs: Showcase
arXiv is surrounded by a community of researchers and developers working at the cutting edge of information science and technology.

https://info.arxiv.org/labs/showcase.html


## arXiv API User's Manual
https://info.arxiv.org/help/api/user-manual.html

Please review the [Terms of Use for arXiv APIs](https://info.arxiv.org/help/api/tou.html) before using the arXiv API.


you can search for articles that contain electron AND proton with the API by entering

http://export.arxiv.org/api/query?search_query=all:electron+AND+all:proton

The parameters for each of the API methods are explained below. For each method, the base url is
```
http://export.arxiv.org/api/{method_name}?{parameters}
```

|     |     |     |     |     |
| --- | --- | --- | --- | --- |
| query |     |     |     |     |
|     | **parameters** | **type** | **defaults** | **required** |
|     | `search_query` | string | None | No  |
|     | `id_list` | comma-delimited string | None | No  |
|     | `start` | int | 0   | No  |
|     | `max_results` | int | 10  | No  |

### Details of Query Construction

|     |     |
| --- | --- |
| **prefix** | **explanation** |
| ti  | Title |
| au  | Author |
| abs | Abstract |
| co  | Comment |
| jr  | Journal Reference |
| cat | Subject Category |
| rn  | Report Number |
| id  | Id (use `id_list` instead) |
| all | All of the above |

### start and max_results paging
```
http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=10 (1)
http://export.arxiv.org/api/query?search_query=all:electron&start=10&max_results=10 (2)
http://export.arxiv.org/api/query?search_query=all:electron&start=20&max_results=10 (3)
```

    Get results 0-9

    Get results 10-19

    Get results 20-29

A request with `max_results >30,000` will result in an `HTTP 400 error code` with appropriate explanation. A request for 30000 results will typically take a little over 2 minutes to return a response of over 15MB. Requests for fewer results are much faster and correspondingly smaller.

### sort order for return results

There are two options for for the result set to the API search, sortBy and sortOrder.

sortBy can be "relevance", "lastUpdatedDate", "submittedDate"

sortOrder can be either "ascending" or "descending"

A sample query using these new parameters looks like:
```
http://export.arxiv.org/api/query?search_query=ti:"electron thermal conductivity"&sortBy=lastUpdatedDate&sortOrder=ascending
```
### The API Response

```xml
    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/" xmlns:arxiv="http://arxiv.org/schemas/atom">
      <link xmlns="http://www.w3.org/2005/Atom" href="http://arxiv.org/api/query?search_query=all:electron&amp;id_list=&amp;start=0&amp;max_results=1" rel="self" type="application/atom+xml"/>
      <title xmlns="http://www.w3.org/2005/Atom">ArXiv Query: search_query=all:electron&amp;id_list=&amp;start=0&amp;max_results=1</title>
      <id xmlns="http://www.w3.org/2005/Atom">http://arxiv.org/api/cHxbiOdZaP56ODnBPIenZhzg5f8</id>
      <updated xmlns="http://www.w3.org/2005/Atom">2007-10-08T00:00:00-04:00</updated>
      <opensearch:totalResults xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">1000</opensearch:totalResults>
      <opensearch:startIndex xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">0</opensearch:startIndex>
      <opensearch:itemsPerPage xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">1</opensearch:itemsPerPage>
      <entry xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
        <id xmlns="http://www.w3.org/2005/Atom">http://arxiv.org/abs/hep-ex/0307015</id>
        <published xmlns="http://www.w3.org/2005/Atom">2003-07-07T13:46:39-04:00</published>
        <updated xmlns="http://www.w3.org/2005/Atom">2003-07-07T13:46:39-04:00</updated>
        <title xmlns="http://www.w3.org/2005/Atom">Multi-Electron Production at High Transverse Momenta in ep Collisions at
      HERA</title>
        <summary xmlns="http://www.w3.org/2005/Atom">  Multi-electron production is studied at high electron transverse momentum in
    positron- and electron-proton collisions using the H1 detector at HERA. The
    data correspond to an integrated luminosity of 115 pb-1. Di-electron and
    tri-electron event yields are measured. Cross sections are derived in a
    restricted phase space region dominated by photon-photon collisions. In general
    good agreement is found with the Standard Model predictions. However, for
    electron pair invariant masses above 100 GeV, three di-electron events and
    three tri-electron events are observed, compared to Standard Model expectations
    of 0.30 \pm 0.04 and 0.23 \pm 0.04, respectively.
    </summary>
        <author xmlns="http://www.w3.org/2005/Atom">
          <name xmlns="http://www.w3.org/2005/Atom">H1 Collaboration</name>
        </author>
        <arxiv:comment xmlns:arxiv="http://arxiv.org/schemas/atom">23 pages, 8 figures and 4 tables</arxiv:comment>
        <arxiv:journal_ref xmlns:arxiv="http://arxiv.org/schemas/atom">Eur.Phys.J. C31 (2003) 17-29</arxiv:journal_ref>
        <link xmlns="http://www.w3.org/2005/Atom" href="http://arxiv.org/abs/hep-ex/0307015v1" rel="alternate" type="text/html"/>
        <link xmlns="http://www.w3.org/2005/Atom" title="pdf" href="http://arxiv.org/pdf/hep-ex/0307015v1" rel="related" type="application/pdf"/>
        <arxiv:primary_category xmlns:arxiv="http://arxiv.org/schemas/atom" term="hep-ex" scheme="http://arxiv.org/schemas/atom"/>
        <category term="hep-ex" scheme="http://arxiv.org/schemas/atom"/>
      </entry>
    </feed>

```


The `<category>` element is used to describe either an arXiv, ACM, or MSC classification. See the [arXiv metadata explanation]() for more details about these classifications.

```
http://export.arxiv.org/api/query?search_query=au:del_maestro+AND+ti:%22quantum+criticality%22
```
This query returns one result, and notice that the feed `<title>` contains double quotes as expected. The table below lists the two grouping operators used in the API.

|     |     |     |
| --- | --- | --- |
| **symbol** | **encoding** | **explanation** |
| ( ) | %28 %29 | Used to group Boolean expressions for Boolean operator precedence. |
| double quotes | %22 %22 | Used to group multiple words into phrases to search a particular field. |
| space | +   | Used to extend a `search_query` to include multiple fields. |

### arXiv identifier scheme - information for interacting services
https://info.arxiv.org/help/arxiv_identifier_for_services.html


The table below shows the correspondence between old and new identifier forms, internal and external identifiers, and semantics that can and cannot be derived from the identifier:

|     | Internal identifier | Preferred external  <br>identifier | Year | Month | Version | Original primary  <br>classification | Primary classification | Secondary classification |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Old scheme | hep-th/9901001  <br>hep-th/9901001v1  <br>math.CA/0611800v2 | arXiv:hep-th/9901001  <br>arXiv:hep-th/9901001v1  <br>arXiv:math/0611800v2 | 1999  <br>1999  <br>2006 | 1 (Jan)  <br>1 (Jan)  <br>11 (Nov) | latest  <br>v1  <br>v2 | hep-th  <br>hep-th  <br>math.CA | (in metadata) | (in metadata) |
| New scheme | 0704.0001  <br>0704.0001v1  <br>1412.7878  <br>1501.00001  <br>9912.12345v2 | arXiv:0704.0001  <br>arXiv:0704.0001v1  <br>arXiv:1412.7878  <br>arXiv:1501.00001  <br>arXiv:9912.12345v2 | 2007  <br>2007  <br>2014  <br>2015  <br>2099 | 6 (Jun)  <br>6 (Jun)  <br>12 (Dec)  <br>1 (Jan)  <br>12 (Dec) | latest  <br>v1  <br>latest  <br>latest  <br>v2 | (in announcement log) | (in metadata) | (in metadata) |

### URLs for standard arXiv functions
The URL patterns for all standard arXiv functions are consistent for the different forms of the arXiv identifier. Some examples are given in the table below:

|     | Generic | Example with old id (9107-0703) | Example with new id (0704-1412) | Example new id (1501-) |
| --- | --- | --- | --- | --- |
| Abstract (normal HTML) | `/abs/id` | `/abs/hep-th/9901001` | `/abs/0706.0001` | `/abs/1501.00001` |
| Abstract (raw txt) | `/abs/id?fmt=txt` | `/abs/hep-th/9901001?fmt=txt` | `/abs/0706.0001?fmt=txt` | `/abs/1501.00001?fmt=txt` |
| PDF | `/pdf/id.pdf` | `/pdf/hep-th/9901001.pdf` | `/pdf/0706.0001.pdf` | `/pdf/1501.00001.pdf` |
| PS  | `/ps/id` | `/ps/hep-th/9901001` | `/ps/0706.0001` | `/ps/1501.00001` |
| Source (.gz,.tar.gz,.pdf...) | `/src/id` | `/src/hep-th/9901001` | `/src/0706.0001` | `/src/1501.00001` |
| Trackbacks | `/tb/id` | `/tb/hep-th/9901001` | `/tb/0706.0001` | `/tb/1501.00001` |
| New listings | `/list/arch-ive/new` | `/list/hep-th/new` | `/list/hep-th/new` | `/list/hep-th/new` |
| Month listings | `/list/arch-ive/yymm` | `/list/hep-th/0601` | `/list/hep-th/0601` | `/list/hep-th/0601` |

# CrossRef
![](https://assets.crossref.org/logo/crossref-logo-200.svg)
[Crossref](https://www.crossref.org/) makes research objects easy to find, cite, link, assess, and reuse. We’re a not-for-profit membership organization that exists to make scholarly communications better.

Crossref was founded in 2000 by some established scientific societies and publishers. 

Crossref is the world’s largest registry of Digital Object Identifiers (DOIs) and metadata for the scholarly research community. Unlike other DOI agencies, we encompass all research stakeholders and all geographies. We facilitate an average of 1.1 billion DOI resolutions (clicks of a DOI link) every month, which is 95% of all DOI activity. And our APIs see over 1 billion queries of our metadata every month.

[A non-technical introduction to our AP](https://www.crossref.org/documentation/retrieve-metadata/rest-api/a-non-technical-introduction-to-our-api/)

[Crossref Unified Resource API *swagger-docs*](https://api.crossref.org/swagger-ui/index.html)

[rest-api-doc](https://github.com/CrossRef/rest-api-doc)
  Documentation for Crossref's REST API. For questions or suggestions, see https://community.crossref.org/ 

## Metadata Retrieval
    Analyse Crossref metadata to inform and understand research

https://www.crossref.org/documentation/retrieve-metadata/

Here is a comparison of the metadata retrieval options. Please note that all interfaces include Crossref test prefixes: 10.13003, 10.13039, 10.18810, 10.32013, 10.50505, 10.5555, 10.88888.


| Feature / option | Metadata Search | Simple Text Query | REST API | XML API | OAI-PMH | OpenURL | Public data files | Metadata Plus (OAI-PMH + REST API) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Interface for people or machines? | People | People | People (low volume and occasional use) and machines | Machines | Machines | Machines | Machines | Machines |
| Output format | Text, JSON | Text | JSON | XML | XML | XML | json.tar.gz | JSON, XML |
| Suitable for citation matching? | Yes (low volume) | Yes | Yes | Yes | No  | No  | Yes, locally | Yes |
| Supports volume downloads? | No  | No  | Yes | No  | Yes | No  | Yes, exclusively | Yes |
| Suitable for usage type | Frequent and occasional | Frequent and occasional | Frequent and occasional | Frequent | Frequent | Frequent | Occasional | Frequent and occasional |
| Free or cost? | Free | Free | Free and cost options | Free and cost options | Cost for full service, more options available | Free | Free | Cost |
| Includes all available metadata? | In JSON only | DOIs only | Yes | Yes | Yes | [Bibliographic](/documentation/content-registration/descriptive-metadata/) only | Yes | Yes |
| Documentation | [Metadata Search](/documentation/retrieve-metadata#00358) | [Simple Text Query](/documentation/retrieve-metadata#00358) | [REST API](/documentation/retrieve-metadata/rest-api) | [XML API](/documentation/retrieve-metadata/xml-api/) | [OAI-PMH](/documentation/retrieve-metadata/oai-pmh) | [OpenURL](/documentation/retrieve-metadata/openurl) | [Tips for working with Crossref public data files and Plus snapshots](https://www.crossref.org/documentation/retrieve-metadata/rest-api/tips-for-using-public-data-files-and-plus-snapshots/) | [Metadata Plus](/documentation/metadata-plus/) ([OAI-PMH](/documentation/retrieve-metadata/oai-pmh) \+ [REST API](/documentation/retrieve-metadata/rest-api)) |

## OpenURL
https://www.crossref.org/documentation/retrieve-metadata/openurl/

Access to the OpenURL service is free, but does ask that you identify yourself. TYou should do this by using your email address to identify yourself. You do not need to register your email address with us in advance, but you do need to include your email address in your query. Find out more.

## Relationships
https://www.crossref.org/documentation/retrieve-metadata/relationships/

Research doesn’t stand alone and relationships show the connections between research outputs, people, and organizations. We deliver these connections via a [relationships API endpoint](https://api.crossref.org/beta/relationships), which makes the [Research Nexus](https://www.crossref.org/documentation/research-nexus/) visible.


[What types of records can be registered with Crossref?](https://www.crossref.org/documentation/research-nexus/)

- Books, chapters, and reference works: includes book title and/or chapter-level records. Books can be registered as a monograph, series, or set.
- Conference proceedings: information about a single conference and records for each conference paper/proceeding.
- Datasets: includes database records or collections.
- Dissertations: includes single dissertations and theses, but not collections.
- Grants: includes both direct funding and other types of support such as the use of equipment and facilities.
- Journals and articles: at the journal title and article level, and includes supplemental materials as components.
- Peer reviews: any number of reviews, reports, or comments attached to any other work that has been registered with Crossref.
- Pending publications: a temporary placeholder record with minimal metadata, often used for embargoed work where a DOI needs to be shared before the full content is made available online.
- Preprints and posted content: includes preprints, eprints, working papers, reports, and other types of content that has been posted but not formally published.
- Reports and working papers: this includes content that is published and likely has an ISSN.
- Standards: includes publications from standards organizations.
- You can also establish relationships between different research objects (such as preprints, translations, and datasets) in your metadata.


# Elsevier Developer Portal - Interactive Scopus APIs
https://dev.elsevier.com/scopus.html


Scopus delivers a comprehensive view of the world of research.
Scopus.com allows you to track analyze and visualize research data from 5000 different publishers.

It covers 78 million items including records from journals, books and book series, conference proceedings and trade publications across 16 million Author Profiles and 70,000 Institutional Profiles All of this comes together to power your research and help you to stay abreast with current publications, find co-authors, analyze journals to publish in and track and monitor global trends

Scopus APIs expose curated abstracts and citation data from all scholarly journals indexed by Scopus[.](https://dev.elsevier.com/sc_apis.html)

# Altmetric API
https://www.altmetric.com/solutions/altmetric-api/#

https://api.altmetric.com/

Yes, **Altmetric provides a public API** that you can use to retrieve the **Altmetric Attention Score and related data** for a research article using its **DOI**.

---

### ✅ **API Overview:**

* **Base URL** (for public access):

  ```
  https://api.altmetric.com/v1/doi/{DOI}
  ```

* **Example** (for a known DOI):

  ```
  https://api.altmetric.com/v1/doi/10.1038/nature12373
  ```

* This will return a JSON response with:

  * `altmetric_score`
  * `title`
  * `journal`
  * `cited_by_tweeters_count`, `cited_by_news_outlets_count`, etc.
  * `images`, `donut`, and other metadata

---

### 🔒 Rate Limiting & API Key:

* The **public API** is free but **rate-limited**.
* For **higher usage or commercial access**, you need to:

  * Contact [Altmetric](https://www.altmetric.com/)
  * Get an **API key**
  * Use their **authenticated API** for bulk or advanced queries

---

### 🔧 Example (Python):

```python
import requests

doi = "10.1038/nature12373"
url = f"https://api.altmetric.com/v1/doi/{doi}"

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    print("Altmetric Score:", data.get("score"))
else:
    print("Error:", response.status_code)
```

