from datetime import datetime

from pydantic import BaseModel, PositiveInt


class Movie(BaseModel):
    ID: PositiveInt  # incremental primary key
    CreatedAt: datetime  # when the movie was added to the DB
    Title: str  # movie title
    Year: PositiveInt  # movie release year
    Runtime: PositiveInt  # runtime in minutes
    Genres: list[str]  # list of genres used to categorize movie
    Version: (
        PositiveInt  # incremental integer updated every time the movie data is updated
    )
