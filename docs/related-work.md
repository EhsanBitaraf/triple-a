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


## OpenAlex
OpenAlex is a free and open catalog of the global research system. It's named after the ancient Library of Alexandria and made by the nonprofit OurResearch.

This is the help center for OpenAlex, containing information about the data, the website where you can start exploring, and the background concepts. To learn about the API, the data snapshot, and other fun stuff, head over to our technical documentation.

At the heart of OpenAlex is our dataset—a catalog of works. A work is any sort of scholarly output. A research article is one kind of work, but there are others such as datasets, books, and dissertations. We keep track of these works—their titles (and abstracts and full text in many cases), when they were created, etc. But that's not all we do. We also keep track of the connections between these works, finding associations through things like journals, authors, institutional affiliations, citations, concepts, and funders. There are hundreds of millions of works out there, and tens of thousands more being created every day, so it's important that we have these relationships to help us make sense of research at a large scale.

This type of data is a valuable resource to institutions, researchers, governments, publishers, funders, and anyone else interested in global research and scholarly communication. We offer the data freely so that its value can be shared. Using the website, anyone can get started right away exploring the data to learn about all sorts of things, from individual papers, to global research trends.

[OurResearch](https://ourresearch.org/) is a nonprofit that builds tools for Open Science, including OpenAlex, Unpaywall, and Unsub, among others. Our open-source tools are used by millions every day, in universities, businesses, and libraries worldwide, to uncover, connect, and analyze research products.

Openness is one of our core values, and so we strive to bake it into everything we do—including our data, code, software, and organizational practices. This is also why OpenAlex is completely open-source and free to use under the CC0 license.

OpenAlex offers an open replacement for industry-standard scientific knowledge bases like Elsevier's Scopus and Clarivate's Web of Science. Compared to these paywalled services, OpenAlex offers significant advantages in terms of inclusivity, affordability, and availability.

[API of OpenAlex](https://docs.openalex.org/)

https://help.openalex.org/hc/en-us


# Article

## pyBibX - A Python Library for Bibliometric and Scientometric Analysis Powered withArtificial Intelligence Tools
[link](https://www.researchgate.net/publication/370417659_pyBibX_--_A_Python_Library_for_Bibliometric_and_Scientometric_Analysis_Powered_with_Artificial_Intelligence_Tools?isFromSharing=1)

# Opensource

## TechMiner development branch 
Analysis of bibliographic datasets using Python

TechMiner is a package for mining relevant information about topics related to Research and Development (R&D) literature extracted from bibliographical databases as Scopus. 

[GitHub](https://github.com/ElsevierSoftwareX/SOFTX-D-21-00031)

[Document](https://jdvelasq.github.io/techminer/)

[Article](https://www.sciencedirect.com/science/article/pii/S235271102300153X)

## PyblioNet
PyblioNet is a software tool for the creation, visualization and analysis of bibliometric networks based on [Pybliometrics](https://pybliometrics.readthedocs.io/en/stable/), NetworkX and VisJs. It combines a Python-based data collection tool that accesses the Scopus database with a browser-based visualization and analysis tool. It allows users to create networks of publication data based on citations, co-citations, shared authors, bibliographic coupling, and shared keywords.


[GitHub](https://github.com/Mat-Mueller/PyblioNet)


[Article](https://www.sciencedirect.com/science/article/pii/S2352711023002613) 
PyblioNet – Software for the creation, visualization and analysis of bibliometric networks



## metaknowledge
A Python library for doing bibliometric and network analysis in science and health policy research 

https://github.com/UWNETLAB/metaknowledge


## Tethne: Bibliographic Network Analysis in Python
Tethne provides tools for easily parsing and analyzing bibliographic data in Python. The primary emphasis is on working with data from the ISI Web of Science database, and providing efficient methods for modeling and analyzing citation-based networks. Future versions will include support for PubMed, Scopus, and other databases.

As of v0.3, Tethne is beginning to include methods for incorporating data from the [JSTOR Data-for-Research service](https://about.jstor.org/whats-in-jstor/text-mining-support/), and [MALLET topic modeling](https://mimno.github.io/Mallet/topics).

https://pythonhosted.org/tethne/index.html

https://github.com/diging/tethne

## Pubmed Parser: A Python Parser for PubMed Open-Access XML Subset and MEDLINE XML Dataset
A Python Parser for PubMed Open-Access XML Subset and MEDLINE XML Dataset 

https://github.com/titipata/pubmed_parser

## PaperBot
open-source web-based search and metadata organization of scientific literature 

https://pubmed.ncbi.nlm.nih.gov/30678631/

https://github.com/NeuroMorphoOrg/PaperBot

## Paperfetcher
Paperfetcher: A tool to automate handsearching and citation searching for systematic reviews

https://onlinelibrary.wiley.com/doi/epdf/10.1002/jrsm.1604

https://paperfetcher.github.io/

https://github.com/paperfetcher/paperfetcher-web-app

https://github.com/paperfetcher/paperfetcher


## paperscraper
![Awesome Badges](https://img.shields.io/badge/badges-awesome-green.svg)
Tools to scrape publication metadata from pubmed, arxiv, medrxiv and chemrxiv. 

Since v0.2.4 paperscraper also supports scraping PDF files directly! Thanks to @daenuprobst for suggestions!

https://github.com/PhosphorylatedRabbits/paperscraper

## bibliometrix: An R-tool for comprehensive science mapping analysis

https://www.sciencedirect.com/science/article/abs/pii/S1751157717300500


https://www.bibliometrix.org/home/

Numerous software tools support bibliometric analysis; however, many of these do not assist scholars in a complete recommended workflow. The most relevant tools are CitNetExplorer (van Eck & Waltman, 2014), VOSviewer (van Eck & Waltman, 2010), SciMAT (Cobo, López-Herrera, Herrera-Viedma, & Herrera, 2012), BibExcel (Persson, Danell, & Schneider, 2009), Science of Science (Sci2) Tool (Sci2 Team, 2009), CiteSpace (Chen, 2006), and VantagePoint (www.thevantagepoint.com).


# Software

## The Science of Science (Sci2) Tool 
The Science of Science (Sci2) Tool is a modular toolset specifically designed for the study of science. It supports the temporal, geospatial, topical, and network analysis and visualization of scholarly datasets at the micro (individual), meso (local), and macro (global) levels.

https://sci2.cns.iu.edu/user/index.php

https://github.com/CIShell/sci2

https://github.com/CIShell/sci2-docker-vnc

# Reference

Tools to visualize connections between academic publications

https://proto-knowledge.blogspot.com/2015/02/tools-to-visualize-connections-between.html
