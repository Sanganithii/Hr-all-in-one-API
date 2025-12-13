from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = "sqlite:///./hr.db"

engine = create_engine(DATABASE_URL)
session = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()    

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()