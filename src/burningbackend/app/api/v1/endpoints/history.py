from burningbackend.app.models.history import History, UpdateHistory

from fastapi import APIRouter
from fastapi import HTTPException


router = APIRouter()

@router.get("/", response_description="History retrieved")
async def get_history(movie: str = None) -> list[history]:
    if movie is None:
        history = await history.all().to_list()
        return history
    else:
        #TODO

@router.post("/", response_description="History Item added to the database")
async def add_history(history: History) -> dict:
    #TODO

@router.post("/cancel/", response_description="Canceled booked order")
async def add_history(_id: str, iscancled: bool = True) -> dict:
    #TODO