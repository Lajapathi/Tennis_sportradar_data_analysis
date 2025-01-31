from unittest.mock import Base
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String,ForeignKey, BigInteger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship

# pgadmin credentials

host='localhost'
port=5432
dbname='Tennis'
user='postgres'
password='laja1103'

# create engine / database connection

engine_string=f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
engine=create_engine(engine_string)


Base=declarative_base()

class competitors_table(Base):
    __tablename__ = 'competitors_table'

    competitor_id = Column(String, primary_key=True)
    name = Column(String)
    country = Column(String)
    country_code = Column(String)
    abbreviation = Column(String)
    

class competitor_rankings_table(Base):
    __tablename__ = 'competitor_rankings_table'

    
    rank = Column(BigInteger,primary_key=True)
    movement = Column(BigInteger)
    points = Column(BigInteger)
    competitions_played = Column(BigInteger)
    competitor_id = Column(String)
    

##Create the tables in the database
Base.metadata.create_all(engine)

# Set up the session
Session = sessionmaker(bind=engine)
session = Session()


competitors_table_list = session.query(competitors_table).all()
competitor_rankings_table_list = session.query(competitor_rankings_table).all()

def get_db_data():# function to return the data from the database
    return session,competitors_table,competitor_rankings_table



