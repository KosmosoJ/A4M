from sqlalchemy import Integer, String, Date, Column, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)

    anime = relationship("Anime", back_populates="anime_r", lazy="joined")


class Anime(Base):
    __tablename__ = "anime"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String)
    russ_name = Column(String)
    type = Column(String)
    started = Column(Date)
    ended = Column(Date)
    rating = Column(Float, default=0)
    seasons = Column(Integer)
    category = Column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )
    anime_r = relationship('Category', back_populates='anime')
