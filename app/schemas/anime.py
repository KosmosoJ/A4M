from pydantic import BaseModel, Field
from datetime import date

class AnimeBase(BaseModel):
    name:str = Field(default='string')
    description:str = Field(default='some description for anime')
    russ_name:str = Field(default='string')
    type:str = Field(default='anime_type')
    started:date = Field(default='2024-12-20')
    ended:date = Field(default='2024-12-20')
    rating:float = Field(default=0)
    seasons:int = Field(default=1)
    slug:str = Field(default='anime-slug')
    category:int = Field(default=1)
    