from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


#creates a class called base
Base = declarative_base()

#create user,task,categories(tables)
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    #relationships
    tasks = relationship("Task", back_populates="user") #relationship btwn user and task
    
    
class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    due_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    priority = Column(Integer, default=2) # 1=low,2=medium,3=high
    status = Column(Boolean, default=False) # true= complete, false= pending 
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    #relationships
    user = relationship("User", back_populates="tasks") #relationship btw a task and user(many task = one user)
    category = relationship("Category", back_populates="tasks") #relationship btw a task and category
    
    
class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    #relationships
    tasks = relationship("Task", back_populates="category")
    



#create an engine to connect to sqlite database
engine = create_engine('sqlite:///tasks.db')

#create all tables
Base.metadata.create_all(engine)

