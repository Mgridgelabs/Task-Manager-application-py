#handles session creation for sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base 

#engine
engine = create_engine('sqlite:///tasks.db')

#creates session class
session = sessionmaker(bind=engine)

#new session 
def create_session():
    return session()

#init database
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    print("Database initialized.")