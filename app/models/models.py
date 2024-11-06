from sqlalchemy import Integer, String, Date, Column, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    slug = Column(String, nullable=True, default=None)
    anime = relationship("Anime", back_populates="anime_r", lazy="joined")

    def __repr__(self) -> str:
        return f'Category(id={self.id!r}, name={self.name!r})'

    def to_dict(self):
        return{
            'id':self.id,
            'name':self.name,
            'slug':self.slug,
        }
        

class Anime(Base):
    __tablename__ = "anime"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String)
    russ_name = Column(String)
    type = Column(String)
    started = Column(Date)
    ended = Column(Date)
    description = Column(String, nullable=True)
    rating = Column(Float, default=0)
    seasons = Column(Integer)
    slug = Column(String, nullable=True, default=None)
    category = Column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )
    episodes = Column(Integer, nullable=True, default=1)
    shiki_id = Column(Integer, nullable=True)
    shiki_url = Column(String, nullable=True)
    animego_url = Column(String, nullable=True)
    anime_r = relationship('Category', back_populates='anime', lazy='joined')
    
    def to_dict(self):
        return{
            'id':self.id,
            'name':self.name,
            'russ_name':self.russ_name,
            'type':self.type,
            'started':f'{self.started}',
            'ended':f'{self.ended}',
            'description':self.description,
            'rating':self.rating,
            'seasons':self.seasons,
            'slug':self.slug,
            'category':self.category,
            'episodes':self.episodes,
            'shiki_id':self.shiki_id,
            'shiki_url':self.shiki_url,
            'animego_url':self.animego_url
        }


class Screenshot(Base):
    __tablename__ = 'screenshots'
    
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    preview = Column(String)
    original = Column(String)
    anime = Column(ForeignKey('anime.id', ondelete='CASCADE')) 
    
    def to_dict(self):
        return{
            'id': self.id,
            'preview': self.preview,
            'original': self.original,
            'anime': self.anime,
        }
    
class Image(Base):
    __tablename__ = 'images'
    
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    preview = Column(String)
    original = Column(String)
    anime = Column(ForeignKey('anime.id', ondelete='CASCADE')) 
    
    def to_dict(self):
        return {
            'id':self.id,
            'preview':self.preview,
            'original':self.original,
            'anime': self.anime,
        }
    
    # anime = relationship("Anime", back_populates="image")
