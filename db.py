from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import settings


engine_db = create_engine(f'postgres://{settings.LOGIN_DB}:{settings.PASS_DB}@{settings.HOST_DB}/{settings.NAME_DB}')
db_session = scoped_session(sessionmaker(bind=engine_db))

Base = declarative_base()
Base.query = db_session.query_property()