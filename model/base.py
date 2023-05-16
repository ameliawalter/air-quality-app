from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

Base = declarative_base()
dir_path = Path(__file__).parent
db_path = dir_path / 'airquality.db'
engine = create_engine(f'sqlite:///{db_path}')
Session = scoped_session(sessionmaker(bind=engine))

