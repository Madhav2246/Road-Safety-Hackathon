from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime, os

DATABASE_URL = os.environ.get("DATABASE_URL","sqlite:///backend/data/sor_db.sqlite")
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class SORFile(Base):
    __tablename__ = "sor_files"
    id = Column(Integer, primary_key=True)
    file_name = Column(String)
    year = Column(Integer)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    source_url = Column(String, nullable=True)

class SORItem(Base):
    __tablename__ = "sor_items"
    id = Column(Integer, primary_key=True)
    sor_file_id = Column(Integer, ForeignKey("sor_files.id"))
    item_code = Column(String)
    description = Column(Text)
    unit = Column(String)
    unit_rate = Column(Float)
    extracted_text = Column(Text)
    page = Column(Integer)
    row_index = Column(Integer)

def init_db():
    Base.metadata.create_all(engine)
