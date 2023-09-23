from datetime import datetime
from typing import Optional
from enum import Enum

from beanie import Document, Indexed
from pydantic.fields import Field
from pydantic import BaseModel


class Category(str, Enum):
    DRINKS = 'Drinks'
    SNACKS = 'Snacks'
    SWEETS = 'Sweets'
    TICKETS = 'Tickets'


class Inventory(Document):
    name: Indexed(str, unique=True)
    amount: int = 0
    price: float
    price_team: float
    amount_sold: int = 0
    category: Category = Category.DRINKS

    class Settings:
        name = "inventory"
        

class UpdateInventory(BaseModel):
    name: Optional[Indexed(str, unique=True)] = None
    amount: Optional[int] = None
    price: Optional[float] = None
    price_team: Optional[float] = None
    amount_sold: Optional[int] = None
    categrory: Optional[Category] = None