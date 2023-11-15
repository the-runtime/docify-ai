from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'docify_users'
    id = Column(String(100), primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100))
    img_url = Column(String(200))
    credits = Column(Integer)
    docify_history = relationship('History', back_populates='user')


class History(Base):
    __tablename__ = 'docify_history'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(100), ForeignKey('docify_users.id'), nullable=False)
    filename = Column(String(100), index=True, nullable=False)
    # file_download_link = Column(String(200), nullable=False)
    gen_time = Column(DateTime, default=datetime.now(), nullable=False)
    user = relationship('User', back_populates='docify_history')
