from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator, field_serializer


# this code was provided by gemini (3 pro)
# it handles custom input format pasring
# this is unused because i disagree with the idea of this custom formatting
# but it is left here because it is useful to understand how this feature is implemented
# maybe i'll add some parsing to allow complex input such as "1 hours" instead of "60" or "60 mins"
def validate_runtime_input(v: Any) -> int:
    """
    Equivalent to Go's UnmarshalJSON.
    Takes a value (likely a string like '102 mins') and returns an int.
    """
    # 1. If it's already an int, just return it (for internal use)
    if isinstance(v, int):
        return v

    # 2. Check if it's a string
    if not isinstance(v, str):
        raise ValueError("invalid runtime format")

    # 3. Split '102 mins' into ['102', 'mins']
    parts = v.split()
    if len(parts) != 2 or parts[1] != "mins":
        raise ValueError("invalid runtime format")

    # 4. Parse the number
    try:
        return int(parts[0])
    except ValueError:
        raise ValueError("invalid runtime format")


# Define the Custom Type
# We use BeforeValidator to parse the string BEFORE Pydantic tries to make it an int.
Runtime = Annotated[int, BeforeValidator(validate_runtime_input)]


class MovieCreate(BaseModel):
    title: str
    year: int
    # This will now accept "102 mins" and turn it into an integer
    runtime: Runtime
    genres: list[str]


class Movie(BaseModel):
    id: int
    title: str
    # You can reuse the logic here or stick to your field_serializer
    runtime: int

    # You already have this 'MarshalJSON' equivalent!
    @field_serializer("runtime")
    def serialize_runtime(self, runtime: int) -> str:
        return f"{runtime} mins"
