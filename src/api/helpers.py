from fastapi import Request
from starlette.routing import Match


def get_allowed_methods(request: Request) -> list[str]:
    """
    Iterates through the app's routes to find all methods supported
    by the path of the current request.
    """
    allowed_methods = set()

    for route in request.app.routes:
        # .matches() checks if the route matches the current request scope
        # Match.PARTIAL indicates the path matched, but the method (or something else) didn't
        match, _ = route.matches(request.scope)
        if match == Match.PARTIAL:
            # route.methods is a set like {'GET', 'POST'}
            if hasattr(route, "methods"):
                allowed_methods.update(route.methods)

    return sorted(list(allowed_methods))
