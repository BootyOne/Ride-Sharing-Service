from fastapi.security import HTTPBearer
from fastapi import Request


class HTTPBearerWithCookie(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(HTTPBearerWithCookie, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        authorization: str = request.headers.get("Authorization")
        cookie_token = request.cookies.get("access_token")

        if not authorization and cookie_token:
            authorization = "Bearer " + cookie_token

        request.state.authorization = authorization  # Здесь мы используем `request.state`

        return await super(HTTPBearerWithCookie, self).__call__(request)


oauth2_scheme = HTTPBearerWithCookie()
