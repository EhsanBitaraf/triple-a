from pydantic import BaseModel,Field
from typing import Optional




class Affiliation(BaseModel):
    HashID : Optional[str]
    Text: Optional[str]  =  Field(description='')
    Part1: Optional[str]  =  Field(description='')
    Part2: Optional[str]  =  Field(description='')
    Part3: Optional[str]  =  Field(description='')
    Part4: Optional[str]  =  Field(description='')
    Part5: Optional[str]  =  Field(description='')
    Part6: Optional[str]  =  Field(description='')
    Has_Extra : Optional[bool] =  Field(description='')
    


class Author(BaseModel):
    HashID : Optional[str]
    LastName: Optional[str]  =  Field(description='contains the surname or the single name used by an individual, even if that single name is not considered to be a surname')
    ForeName: Optional[str]  =  Field(description='contains the remainder of name except for suffix')
    FullName : Optional[str]  =  Field(description='')
    ORCID: Optional[str]  =  Field(description='')
    Affiliations: Optional[list[Affiliation]]  =  Field(description='')


class Article(BaseModel):
    PMID: Optional[str]  =  Field(description='the PubMed (NLM database that incorporates MEDLINE) unique identifier, is a 1 to 8-digit accession number with no leading zeros.')
    DOI: Optional[str]  =  Field(description='')
    Title: Optional[str]  =  Field(description='Article Title contains the entire title of the journal article. Article Title is always in English; those titles originally published in a non-English language and translated for Article Title are enclosed in square brackets.')
    Journal: Optional[str]  =  Field(description='The full journal title (taken from NLM cataloging data following NLM rules for how to compile a serial name) is exported in this element.')
    Authors: Optional[list[Author]] =  Field(description='')
    Abstract: Optional[str]  =  Field(description='')
    OreginalArticle : Optional[dict] =  Field(description='')
    State : Optional[int] =   Field(description='')
    QueryTranslation : Optional[str] =   Field(description='')