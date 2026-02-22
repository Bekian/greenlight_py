import datetime
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, ConfigDict, Field, PositiveInt

from src.internal.data.movies import Movie, MovieResponse

router = APIRouter(prefix="/v1py/movies", tags=["movies"])


class MovieCreate(BaseModel):  # fields are described @ src.internal.data.movies
    # disallow additional fields
    model_config = ConfigDict(extra="forbid")

    title: str = Field(..., min_length=1, max_length=500)
    year: PositiveInt | None = Field(..., gt=1888)
    runtime: PositiveInt | None = Field(..., gt=0)
    genres: set[str] | None = Field(..., min_length=1)


@router.post("")
async def create_movie(movie_input: Annotated[MovieCreate, Body]):
    # will add more later
    return {"message": "movie created", "data": movie_input}


@router.get("/{id}")
async def get_movie(id: int):
    """
    get a movie by id

    this book equivalent of this is called "showMovieHandler"
    """
    # the book has slightly different error behavior here
    # it returns a 404 instead of a 400, i think 400 is more correct so we'll stick with that.
    if id < 1:
        # return 400 response
        raise HTTPException(
            status_code=400,
            detail="Invalid ID provided, only positive integers allowed.",
        )

    # also do if int_id not in movies[] catch to return a 404

    # dummy movie value
    movie = Movie(
        id=id,
        _created_at=datetime.datetime.now(),
        title="Casablanca",
        runtime=102,
        year=None,  # this will be updated
        genres=["romance", "drama", "war"],
        version=1,
    )

    return MovieResponse(movie=movie).model_dump(exclude_none=True)
