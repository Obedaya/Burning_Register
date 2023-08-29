from datetime import datetime
from typing import Optional

from beanie import Document, Indexed
from pydantic.fields import Field



class Movie(Document):
    name: Indexed(str, unique=True)
    datetime: datetime
    room: str


    class Settings:
        name = "movies"
        