from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///C:\\users\\rseethar\\test.db'

engine = create_engine(DATABASE_URL)
Session = scoped_session(sessionmaker(bind=engine))