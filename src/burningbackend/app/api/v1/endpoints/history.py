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
        history = await history.find({"movie": movie}).to_list()
        return history

@router.post("/", response_description="History Item added to the database")
async def add_history(history: History) -> dict:
    await history.create()
    history = await History.find_one({"name": history.name})
    return {"message": "History added successfully", "data": history}

@router.post("/cancel/", response_description="Canceled booked order")
async def add_history(_id: str, iscancled: bool = True) -> dict:
    history = await History.get(_id)
    if not history:
        raise HTTPException(
            status_code=404,
            detail="History record not found"
        )
    history.iscancled = iscancled
    await history.save()
    return {"message": "History updated successfully", "data": history}