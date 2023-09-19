from burningbackend.app.models.movie import Movie, UpdateMovie

from fastapi import APIRouter
from fastapi import HTTPException

router = APIRouter()

@router.post("/", response_description="Movie added to the database")
async def add_movie(movie: Movie) -> dict:
    await movie.create()
    movie = await Movie.find_one({"name": movie.name})
    return {"message": "Movie added successfully", "data": movie}

@router.get("/", response_description="Movies retrieved")
async def get_movies() -> list[Movie]:
    movies = await Movie.all().to_list()
    return movies

@router.get("/name/{name}", response_description="Movie retrieved")
async def get_movie_by_name(name: str) -> Movie:
    movie = await Movie.find_one({"name": name})
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie
@router.get("/{id}", response_description="Movie retrieved")
async def get_movie(id: str) -> Movie:
    movie = await Movie.get(id)
    return movie

@router.put("/{id}", response_description="Movie data updated")
async def update_movie(id: str, req: UpdateMovie) -> dict:
    req = {k: v for k, v in req.dict().items() if v is not None}
    update_query = {"$set": {
        field: value for field, value in req.items()
    }}
    movie = await Movie.get(id)
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie record not found"
        )
    updated_movie = await movie.update(update_query)
    return {"message": "Movie updated successfully", "data": updated_movie}

@router.delete("/{id}", response_description="Movie deleted from the database")
async def delete_movie(id: str) -> dict:
    movie = await Movie.get(id)
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie record not found!"
        )
    await movie.delete()
    return {"message": "Movie deleted successfully"}
