import datetime as dt
from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class BlogPost:
    id: str
    title: str
    content: str
    creation_date: dt.date
