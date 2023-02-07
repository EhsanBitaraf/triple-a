from pydantic import BaseModel,Field
from typing import Optional


class Article(BaseModel):
    PMID: Optional[str]  =  Field(description='the PubMed (NLM database that incorporates MEDLINE) unique identifier, is a 1 to 8-digit accession number with no leading zeros.')
    DOI: Optional[str]  =  Field(description='')
    Title: Optional[str]  =  Field(description='Article Title contains the entire title of the journal article. Article Title is always in English; those titles originally published in a non-English language and translated for Article Title are enclosed in square brackets.')
    Journal: Optional[str]  =  Field(description='The full journal title (taken from NLM cataloging data following NLM rules for how to compile a serial name) is exported in this element.')
    Abstract: Optional[str]  =  Field(description='')
    OreginalArticle : Optional[dict] =  Field(description='')
    State : Optional[int] =   Field(description='')
    QueryTranslation : Optional[str] =   Field(description='')