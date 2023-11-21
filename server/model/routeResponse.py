from datetime import datetime

from pydantic import BaseModel
from typing import List


class Userinfo(BaseModel):
    name: str
    email: str
    credits: int
    imageUrl: str


class singleHistory(BaseModel):
    historyId: int
    filename: str
    fileDownloadLink: str
    generationTime: datetime


class History(BaseModel):
    username: str
    history: List[singleHistory]


class ErrorClass(BaseModel):
    error: List[str]
