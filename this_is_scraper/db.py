from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import UnicodeText
from this_is_scraper.config import DB_URL
from this_is_scraper.config import DEBUG


BASE = declarative_base()


class Articles(BASE):
    __tablename__ = 'articles'
    article_link = Column(String(250), primary_key=True, nullable=False)
    article_dt = Column(DateTime(), nullable=False)
    article_status = Column(String(20), nullable=False)
    article_title = Column(String(150), nullable=True)
    article_content = Column(UnicodeText(), nullable=True)


def get_db_engine():
    engine = create_engine(DB_URL, echo=DEBUG)
    return engine


def get_db_session():
    sessmaker = sessionmaker(bind=get_db_engine())
    session = sessmaker()
    return session


def init_db():
    BASE.metadata.create_all(get_db_engine())
