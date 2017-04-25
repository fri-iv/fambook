from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

# engine = create_engine('sqlite:///test.db', convert_unicode=True)
engine = create_engine('postgresql+psycopg2://server:12345@localhost:5432/test')

Base = declarative_base()

meta = MetaData()
meta.reflect(bind=engine)

db_session = Session(bind=engine)
