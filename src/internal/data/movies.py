from datetime import datetime

from pydantic import BaseModel, PositiveInt


class Movie(BaseModel):
    id: PositiveInt  # incremental primary key
    _created_at: datetime  # when the movie was added to the DB, marked as private and excluded from output
    title: str  # movie title
    year: PositiveInt | None  # movie release year
    runtime: PositiveInt | None  # runtime in minutes
    genres: list[str] | None  # list of genres used to categorize movie
    version: (
        PositiveInt  # incremental integer updated every time the movie data is updated
    )


# these response models contrast the wrapper function used to accomplish the same task in chapter 3.04
# this approach is more intentional and explicit with how wrappers are declared, so we'll be using this approach instead
class MovieResponse(BaseModel):
    movie: Movie  # a single movie


class MoviesResponse(BaseModel):
    movie: list[Movie]  # a list of movies
    metadata: dict  # e.g. pagination info


"""
note from the book about why using private vs json struct tags is better:
Note: You can also prevent a struct field from appearing in the JSON output by simply making it unexported.
But using the json:"-" struct tag is generally a better choice:
    it’s an explicit indication to both Go and any future readers of your code
    that you don’t want the field included in the JSON,
    and it helps prevent problems if someone changes the field to be
    exported in the future without realizing the consequences.

in python we could do this by using a conditional that is always true,
but i think this method + a comment is sufficient
"""
