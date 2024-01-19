
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'mysql+pymysql://root:12345@localhost/expense'

db_engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Corrected line: use db_engine instead of engine
Base.metadata.create_all(bind=db_engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
