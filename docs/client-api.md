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
