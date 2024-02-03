from pydantic import BaseModel, Field
from typing import Optional

# custom_encoder = lambda obj:  dict(_type=type(obj).__name__, **obj.dict())


# It creates a class called Node with the following attributes:
#  Type, Identifier, and Name.
class Node(BaseModel):
    Type: Optional[str] = Field(description="", default=None)
    Identifier: Optional[str] = Field(description="", default=None)
    Name: Optional[str] = Field(description="", default=None)

    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__,
    #         sort_keys=True, indent=4)

    def json(self):
        return {"Type": self.Type, "Identifier": self.Identifier, "Name": self.Name}

    # class Config:
    #     json_encoders = {
    #         Base: custom_encoder
    #     }


# The Edge class is a model that has four fields:
#  HashID, SourceID, DestinationID, and Type
class Edge(BaseModel):
    HashID: Optional[str] = Field(description="", default=None)
    SourceID: Optional[str] = Field(description="", default=None)
    DestinationID: Optional[str] = Field(description="", default=None)
    Type: Optional[str] = Field(description="", default=None)
    Weight: Optional[float] = Field(description="", default=None)
