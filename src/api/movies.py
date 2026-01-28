import datetime

from fastapi import APIRouter, HTTPException

from src.internal.data.movies import Movie

router = APIRouter(prefix="/v1py/movies", tags=["movies"])


@router.post("")
async def create_movie():
    return "create a new movie"


@router.get("/{id}")
async def get_movies(id: int):
    if id < 1:
        raise HTTPException(
            status_code=400,
            detail="Invalid ID provided, only positive integers allowed.",
        )

    # also do if int_id not in movies catch to return a 404

    # dummy movie value
    movie = Movie(
        id=id,
        created_at=datetime.datetime.now(),
        title="Casablanca",
        runtime=102,
        year=None,  # this will be updated
        genres=["romance", "drama", "war"],
        version=1,
    )

    return movie.model_dump(exclude_none=True)
