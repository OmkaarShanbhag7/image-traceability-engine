from sqlalchemy import Column, Integer, String
from database import Base

class ImageRecord(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    phash = Column(String)
