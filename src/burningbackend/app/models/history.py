from datetime import datetime
from typing import Optional, List

from beanie import Document, Indexed
from pydantic.fields import Field
from pydantic import BaseModel

from burningbackend.app.models.inventory import Category

class Product(BaseModel):
    name: str
    amount: int
    price: float
    category: Category


class History(Document):
    timestamp: datetime
    total: float
    isteam: bool 
    movie: str
    cancellation: bool = False
    products: List[Product]


    class Settings:
        name = "history"