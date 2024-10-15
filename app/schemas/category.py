from pydantic import BaseModel, Field


class BaseCategory(BaseModel):
    name:str = Field(default='string')

