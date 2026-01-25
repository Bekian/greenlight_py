from fastapi import APIRouter, HTTPException

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
    return {"value": f"details of movie with ID: {id}"}
