
from sqlalchemy import Column, Integer, String, Text, Date, Float, ForeignKey, ARRAY, TIMESTAMP, create_engine
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    pmid = Column(String(20), unique=True, nullable=False)
    title = Column(Text)
    abstract = Column(Text)
    journal = Column(Text)
    authors = Column(ARRAY(String))
    publication_date = Column(Date)
    source = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    sentiments = relationship("Sentiment", back_populates="article", cascade="all, delete")
    topics = relationship("Topic", back_populates="article", cascade="all, delete")
    sentiment_score = Column(Float)



class Sentiment(Base):
    __tablename__ = 'sentiment'

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('articles.id', ondelete='CASCADE'), nullable=False)
    polarity = Column(Float)
    subjectivity = Column(Float)
    model_version = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())

    article = relationship("Article", back_populates="sentiments")


class Topic(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('articles.id', ondelete='CASCADE'), nullable=False)
    topic_label = Column(String(255))
    score = Column(Float)
    method = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())

    article = relationship("Article", back_populates="topics")
