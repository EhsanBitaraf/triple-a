# Article Analysis Assistant (AAA) Related Work
This program somehow creates a network of article references and provides a connection between authors and keywords, these things are usually called "Citation Graph".

Following are similar cases:

## Semantic Scholar Academic Graph API
Providing a reliable source of scholarly data for developers
This index over 200 million academic papers sourced from publisher partnerships, data providers, and web crawls.

https://www.semanticscholar.org/product/api

## Automatic Generation of Academic Citation Graph
created a tool for you homo academicus to automatically create the said citation graph for any paper. This should be helpful for researchers to catch up on the trend of a rapidly changing field.

First, if you are using Mendeley (or any other Reference Management Software), export your papers as a .bib file which should include the arXiv ID and issue year information. Then, use Mathematica to run the code. It will take you to the Astrophysics Data System of Harvard and find out the list of reference for each paper. Finally, a citation graph will be drawn with the help of Wolfram Language.

https://community.wolfram.com/groups/-/m/t/1770600

https://lanstonchu.wordpress.com/2019/08/20/automatic-generation-of-academic-citation-graph/

https://github.com/lanstonchu/citation-graph

## Astrophysics Data System
![](https://ui.adsabs.harvard.edu/help/common/images/transparent_logo.svg)
The SAO/NASA Astrophysics Data System (ADS) is a digital library portal for researchers in astronomy and physics, operated by the Smithsonian Astrophysical Observatory (SAO) under a NASA grant.

The ADS maintains three bibliographic collections containing more than 15 million records covering publications in astronomy and astrophysics, physics, and general science, including all arXiv e-prints. Abstracts and full-text of major astronomy and physics publications are indexed and searchable through the new ADS modern search form as well as a classic search form. A browsable paper form is also available.

https://ui.adsabs.harvard.edu/

## Connected Papers
Connected Papers is a unique, visual tool to help researchers and applied scientists find and explore papers relevant to their field of work. 

To create each graph, we analyze an order of ~50,000 papers and select the few dozen with the strongest connections to the origin paper. 

Our database is connected to the Semantic Scholar Paper Corpus (licensed under ODC-BY). Their team has done an amazing job of compiling hundreds of millions of published papers across many scientific fields.

https://www.connectedpapers.com/

## Citation graph dbpedia.org
A citation graph (or citation network), in information science and bibliometrics, is a directed graph that describes the citations within a collection of documents. Each vertex (or node) in the graph represents a document in the collection, and each edge is directed from one document toward another that it cites (or vice versa depending on the specific implementation).

https://dbpedia.org/page/Citation_graph

## ResearchRabbit
![](https://images.squarespace-cdn.com/content/v1/5dee82c56fcd7b0290640db5/2d9c67bf-a7e9-4810-8948-45ce24546798/logo.png?format=1500w)

It’s like a second brain to do literature review! It does half the work for you… and makes life a lot easier!

https://www.researchrabbit.ai/

## Network Repository - Citation Networks
https://networkrepository.com/cit.php


## OpenCitations 
Creating an Open Citation Graph from PDF Documents

https://www.ipvs.uni-stuttgart.de/news/news/Creating-an-Open-Citation-Graph-from-PDF-Documents/

OpenCitations is an independent not-for-profit infrastructure organization for open scholarship dedicated to the publication of open bibliographic and citation data by the use of Semantic Web (Linked Data) technologies.

http://opencitations.net/


## metaknowledge
A Python library for doing bibliometric and network analysis in science and health policy research 

https://github.com/UWNETLAB/metaknowledge

# Reference

Tools to visualize connections between academic publications

https://proto-knowledge.blogspot.com/2015/02/tools-to-visualize-connections-between.html
