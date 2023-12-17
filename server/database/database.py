from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, session


class Database:
    _instance = None

    def __new__(cls, db_url=""):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._Engine = create_engine(db_url)
            cls._instance.Base = declarative_base()
            cls._instance.session = sessionmaker(autocommit=False, autoflush=True, bind=cls._instance._Engine)
            cls._instance.Session = cls._instance.session()
        return cls._instance

    def get_session(self) -> session:
        self.Session.rollback()
        return self.Session


