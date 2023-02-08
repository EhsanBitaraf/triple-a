from pydantic import BaseModel,Field
from typing import Optional


# It creates a class called Node with the following attributes: Type, Identifier, and Name.
class Node(BaseModel):
    Type: Optional[str]  =  Field(description='')
    Identifier: Optional[str]  =  Field(description='')
    Name: Optional[str]  =  Field(description='')

# The Edge class is a model that has four fields: HashID, SourceID, DestinationID, and Type
class Edge(BaseModel):
    HashID: Optional[str]  =  Field(description='')
    SourceID: Optional[str]  =  Field(description='')
    DestinationID: Optional[str]  =  Field(description='')
    Type: Optional[str]  =  Field(description='')




