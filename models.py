from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool
import os


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
engine = create_engine('sqlite:///' + os.path.join(APP_ROOT, 'main.db'), 
						connect_args={'check_same_thread':False},
                    	poolclass=StaticPool)
Base = declarative_base()
Session = scoped_session(sessionmaker(bind=engine))

class Info(Base):
	__tablename__ = 'infos'
	id = Column(Integer, primary_key=True)
	chat_id = Column(Integer)	
	name = Column(String(255))
	age = Column(String(255))
	phone = Column(String(255))
	mail = Column(String(255))
	job = Column(String(255))
	like = Column(String(255))
	komun = Column(String(255))
	hobby = Column(String(255))
	district = Column(String(255))
	graf = Column(String(255))
	education = Column(String(255))
