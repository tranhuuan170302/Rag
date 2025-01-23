from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    current_seller = Column(String, nullable=True)
    images = Column(String, nullable=True)
    short_url = Column(String, nullable=True)
    thumbnail_url = Column(String, nullable=True)
    short_description = Column(String, nullable=True)
    description = Column(String, nullable=True)
    rating_average = Column(Float, nullable=True)
    quantity_sold = Column(Integer, nullable=True)
